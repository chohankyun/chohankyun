# -*- coding: utf-8 -*-
import jwt
from calendar import timegm
from datetime import datetime

from chohankyun.settings import JWT_AUTH


class Handler:
    @staticmethod
    def jwt_get_secret_key():
        # 나중에 키 관련 로직 추가
        if JWT_AUTH['JWT_GET_USER_SECRET_KEY']:
            key = str(JWT_AUTH['JWT_GET_USER_SECRET_KEY'])
            return key
        return JWT_AUTH['JWT_SECRET_KEY']

    @staticmethod
    def jwt_payload_handler(obj):
        payload = {
            'id': obj.id,
            'username': obj.username,
            'client_ip': obj.client_ip,
            'exp': datetime.utcnow() + JWT_AUTH['JWT_EXPIRATION_DELTA']
        }

        if JWT_AUTH['JWT_ALLOW_REFRESH']:
            payload['orig_iat'] = timegm(
                datetime.utcnow().utctimetuple()
            )

        if JWT_AUTH['JWT_AUDIENCE']:
            payload['aud'] = JWT_AUTH.JWT_AUDIENCE

        if JWT_AUTH['JWT_ISSUER']:
            payload['iss'] = JWT_AUTH['JWT_ISSUER']

        return payload

    def jwt_encode_handler(self, payload):
        key = JWT_AUTH['JWT_PRIVATE_KEY'] or self.jwt_get_secret_key()
        return jwt.encode(payload, key, JWT_AUTH['JWT_ALGORITHM']).decode('utf-8')

    def jwt_decode_handler(self, token):
        options = {
            'verify_exp': JWT_AUTH['JWT_VERIFY_EXPIRATION'],
        }
        secret_key = self.jwt_get_secret_key()
        return jwt.decode(
            token,
            JWT_AUTH['JWT_PUBLIC_KEY'] or secret_key,
            JWT_AUTH['JWT_VERIFY'],
            options=options,
            leeway=JWT_AUTH['JWT_LEEWAY'],
            audience=JWT_AUTH['JWT_AUDIENCE'],
            issuer=JWT_AUTH['JWT_ISSUER'],
            algorithms=[JWT_AUTH['JWT_ALGORITHM']])

    @staticmethod
    def get_client_ip_address(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0]
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        return client_ip
