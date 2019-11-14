# -*- coding: utf-8 -*-
import jwt
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)

from chohankyun.settings import JWT_AUTH
from shared.handler import Handler


class JWTUser:
    def __init__(self, data):
        self.id = data.get('id')
        self.username = data.get('username')
        self.is_authenticated = True


class BaseJSONWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            handler = Handler()
            payload = handler.jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'Invalid token.'
            raise exceptions.AuthenticationFailed(msg)

        if payload.get('client_ip') != handler.get_client_ip_address(request):
            msg = 'Error decoding data.'
            raise exceptions.AuthenticationFailed(msg)

        user = self.get_user(payload)
        return user, jwt_value

    @staticmethod
    def get_user(payload):
        return JWTUser(payload)


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    www_authenticate_realm = 'api'

    @staticmethod
    def get_jwt_value(request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = JWT_AUTH['JWT_AUTH_HEADER_PREFIX'].lower()

        if not auth:
            if JWT_AUTH['JWT_AUTH_COOKIE']:
                return request.COOKIES.get(JWT_AUTH['JWT_AUTH_COOKIE'])
            return None

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = 'Invalid Authorization header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid Authorization header. Credentials string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_header(self, request):
        return '{0} realm="{1}"'.format(JWT_AUTH['JWT_AUTH_HEADER_PREFIX'], self.www_authenticate_realm)
