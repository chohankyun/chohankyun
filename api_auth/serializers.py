# -*- coding: utf-8 -*-
import random
import string
from datetime import datetime

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.templatetags import l10n
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode as uid_decoder, urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

from api_auth.confirmation import EmailConfirmationHMAC
from shared.email import EmailMixin
from shared.handler import Handler


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = 'Must include "username" and "password".'
            raise exceptions.ValidationError(msg)

        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise exceptions.ValidationError(msg)
            if user.is_staff or user.is_superuser:
                msg = 'You do not have permission to perform this action.'
                raise exceptions.ValidationError(msg)
            if not user.is_email_verified:
                msg = 'Email is not verified.'
                raise exceptions.NotAcceptable(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class JWTSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_user(obj):
        jwt_user = {'id': obj.id, 'username': obj.username, 'is_authenticated': True}
        return jwt_user

    def get_token(self, obj):
        handler = Handler()
        obj.client_ip = handler.get_client_ip_address(self.context.get('request'))
        payload = handler.jwt_payload_handler(obj)
        token = handler.jwt_encode_handler(payload)
        return token


class SessionUserSerializer(serializers.ModelSerializer):
    local_last_login = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'date_joined', 'email', 'local_last_login']

    @staticmethod
    def get_local_last_login(obj):
        return l10n.localize(obj.last_login)


class UsernameFindSerializer(serializers.Serializer, EmailMixin):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        user = self._validate_email(email)

        if not user.is_active:
            msg = 'User account is disabled.'
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

    def save(self):
        self.send_email('auth/username_find_subject.txt', 'auth/username_find_email.html')


class PasswordResetSerializer(serializers.Serializer, EmailMixin):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        user = self._validate_email(email)

        if not user.is_active:
            msg = 'User account is disabled.'
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

    def get_extras(self):
        user = self.validated_data['user']
        return {
            'password': ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': PasswordResetTokenGenerator().make_token(user),
            'host': self.context.get('request').get_host()
        }

    def save(self):
        self.send_email('auth/password_reset_subject.txt', 'auth/password_reset_email.html')


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            msg = _('Invalid uid.')
            raise exceptions.ValidationError(msg)

        if not default_token_generator.check_token(user, attrs['token']):
            msg = _('Invalid token.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

    def save(self):
        password = self.validated_data["password"]
        user = self.validated_data["user"]
        user.set_password(password)
        user.save()


class PasswordChangeSerializer(serializers.Serializer, EmailMixin):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            jwt_user = self.context['request'].user
            user = get_user_model().objects.get(pk=jwt_user.id)
        except get_user_model().DoesNotExist:
            msg = 'User matching query does not exist.'
            raise exceptions.ValidationError(msg)

        if not user.is_active:
            msg = 'User account is disabled.'
            raise exceptions.ValidationError(msg)

        if not user.check_password(attrs['old_password']):
            msg = 'Invalid old password.'
            raise serializers.ValidationError(msg)

        if attrs['new_password1'] != attrs['new_password2']:
            msg = "The two password fields didn't match."
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs

    def get_extras(self):
        return {
            'old_password': self.validated_data['old_password'],
            'new_password': self.validated_data['new_password1']
        }

    def save(self):
        password = self.validated_data["new_password1"]
        user = self.validated_data["user"]
        user.set_password(password)
        user.save()
        self.send_email('auth/password_changed_subject.txt', 'auth/password_changed_email.html')


class RegisterSerializer(serializers.Serializer, EmailMixin):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    @staticmethod
    def validate_username(username):
        user = get_user_model().objects.filter(username=username).first()
        if user:
            msg = 'A user is already registered with this username.'
            raise serializers.ValidationError(msg)
        return username

    @staticmethod
    def validate_email(email):
        user = get_user_model().objects.filter(email=email).first()
        if user:
            msg = 'A user is already registered with this email.'
            raise serializers.ValidationError(msg)
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            msg = "The two password fields didn't match."
            raise serializers.ValidationError(msg)
        return data

    @staticmethod
    def custom_register():
        return {
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
            'is_email_verified': False,
            'date_joined': datetime.now()
        }

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def get_extras(self):
        email = self.validated_data.get('email', '')
        confirmation = EmailConfirmationHMAC(email)
        return {
            'activate_url': confirmation.get_email_confirmation_url(self.context['request'], confirmation)
        }

    def save(self):
        data = self.get_cleaned_data()
        data.update(self.custom_register())
        user = get_user_model()(**data)
        user.set_password(user.password)
        user.save()
        self.validated_data['user'] = user
        self.send_email('auth/email_confirm_subject.txt', 'auth/email_confirm_email.html')


class EmailConfirmSerializer(serializers.Serializer):
    key = serializers.CharField()

    def validate(self, attrs):
        confirmation = EmailConfirmationHMAC.from_key(attrs['key'])
        if not confirmation:
            msg = _('Invalid key.')
            raise exceptions.ValidationError(msg)

        attrs['confirmation'] = confirmation
        return attrs

    def save(self):
        confirmation = self.validated_data["confirmation"]
        confirmation.confirm()
