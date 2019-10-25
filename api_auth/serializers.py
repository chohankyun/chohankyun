# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.templatetags import l10n
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

from chohankyun import settings
from jwt_auth.handler import Handler


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


class UsernameFindSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        user = get_user_model().objects.filter(email=email).first()

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Invalid Email.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

    def save(self):
        self.send_email()

    def send_email(self):
        request = self.context.get('request')
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        user = self.validated_data['user']

        context = {
            'domain': domain,
            'site_name': site_name,
            'user': user,
            'protocol': 'https' if request.is_secure() else 'http',
        }

        subject = loader.render_to_string('registration/username_find_subject.txt', context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string('registration/username_find_email.html', context)
        email_message = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
        email_message.send()
