# -*- coding: utf-8 -*-
import uuid
from calendar import timegm
from datetime import datetime

import jwt
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

# Get the UserModel
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_get_secret_key

UserModel = get_user_model()


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
        data = dict()
        data['id'] = obj.id
        data['username'] = obj.username
        data['is_authenticated'] = True
        return data

    def get_token(self, obj):
        payload = self.jwt_payload_handler(obj)
        token = self.jwt_encode_handler(payload)
        return token

    @staticmethod
    def jwt_payload_handler(obj):
        payload = {
            'id': obj.id,
            'username': obj.username,
            'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
        }

        if api_settings.JWT_ALLOW_REFRESH:
            payload['orig_iat'] = timegm(
                datetime.utcnow().utctimetuple()
            )

        if api_settings.JWT_AUDIENCE is not None:
            payload['aud'] = api_settings.JWT_AUDIENCE

        if api_settings.JWT_ISSUER is not None:
            payload['iss'] = api_settings.JWT_ISSUER

        return payload

    @staticmethod
    def jwt_encode_handler(payload):
        key = api_settings.JWT_PRIVATE_KEY or jwt_get_secret_key(payload)
        return jwt.encode(
            payload,
            key,
            api_settings.JWT_ALGORITHM
        ).decode('utf-8')

