# -*- coding: utf-8 -*-
from django.templatetags import l10n
from rest_framework import serializers
from index.models import Header
from index.models import Footer


class HeaderSerializer(serializers.ModelSerializer):
    local_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Header
        fields = '__all__'
        [fields].append('local_datetime')

    @staticmethod
    def get_local_datetime(obj):
        return l10n.localize(obj.updated_datetime)


class FooterSerializer(serializers.ModelSerializer):
    local_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Footer
        fields = '__all__'
        [fields].append('local_datetime')

    @staticmethod
    def get_local_datetime(obj):
        return l10n.localize(obj.updated_datetime)
