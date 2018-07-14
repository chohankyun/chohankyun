# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.templatetags import l10n


class LocaleDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return l10n.localize(value)