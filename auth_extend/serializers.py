import random
import string

from django.contrib.auth import get_user_model
from django.templatetags import l10n
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers
from chohankyun import settings


class UserDetailsSerializer(serializers.ModelSerializer):
    local_last_login = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'date_joined', 'email', 'local_last_login']

    @staticmethod
    def get_local_last_login(obj):
        return l10n.localize(obj.last_login)


class UsernameFindSerializer(PasswordResetSerializer):
    def create(self, validated_data):
        super(UsernameFindSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        super(UsernameFindSerializer, self).update(validated_data)

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': request,
            'subject_template_name': 'registration/username_find_subject.txt',
            'email_template_name': 'registration/username_find_email.html',
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class PasswordResetExtendSerializer(PasswordResetSerializer):
    def create(self, validated_data):
        super(PasswordResetExtendSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        super(PasswordResetExtendSerializer, self).update(validated_data)

    def get_email_options(self):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return {'extra_email_context': {'password': password, 'host': self.context.get('request').get_host()}}
