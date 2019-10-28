# -*- coding: utf-8 -*-
import random
import string

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.templatetags import l10n
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode as uid_decoder, urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

from jwt_auth.handler import Handler
from chohankyun import settings


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_username(self, username, password):
        if username and password:
            return self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = None

        if username:
            user = self._validate_username(username, password)

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
            if user.is_staff or user.is_superuser:
                msg = _('You do not have permission to perform this action.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
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


class EmailMixin:
    def get_extras(self):
        """Override this method to add extra options"""
        return {}

    @staticmethod
    def validate_email(email):
        user = get_user_model().objects.filter(email=email).first()

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('E-mail address matching query does not exist.')
            raise exceptions.ValidationError(msg)
        return user

    def send_email(self, subject_template_name, email_template_name):
        request = self.context.get('request')
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        user = self.validated_data['user']

        opt = {
            'domain': domain,
            'site_name': site_name,
            'user': user,
            'protocol': 'https' if request.is_secure() else 'http',
        }

        opt.update(self.get_extras())

        subject = loader.render_to_string(subject_template_name, opt)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, opt)
        email_message = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
        email_message.send()


class UsernameFindSerializer(serializers.Serializer, EmailMixin):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        attrs['user'] = self.validate_email(email)
        return attrs

    def save(self):
        self.send_email('registration/username_find_subject.txt', 'registration/username_find_email.html')


class PasswordResetSerializer(serializers.Serializer, EmailMixin):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        attrs['user'] = self.validate_email(email)
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
        self.send_email('registration/password_reset_subject.txt', 'registration/password_reset_email.html')


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form = None

    def validate(self, attrs):
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise exceptions.ValidationError({'uid': ['Invalid value']})

        self.set_password_form = SetPasswordForm(user=user, data=attrs)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(user, attrs['token']):
            raise exceptions.ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer, EmailMixin):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form = None

    def __init__(self, *args, **kwargs):
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (self.user, not self.user.check_password(value))

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = SetPasswordForm(user=self.user, data=attrs)

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def get_extras(self):
        return {
            'old_password': self.validated_data['old_password'],
            'new_password': self.validated_data['new_password']
        }

    def save(self):
        self.set_password_form.save()
        self.send_email('registration/password_changed_subject.txt', 'registration/password_changed_email.html')
