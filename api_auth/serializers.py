# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

from jwt_auth.authentication import JWTUser
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
        obj.client_ip = handler.get_client_ip_address(self.context['request'])
        payload = handler.jwt_payload_handler(obj)
        token = handler.jwt_encode_handler(payload)
        return token
