# -*- coding: utf-8 -*-
from django.templatetags import l10n
from rest_framework import serializers
from board.models import Post


class SearchSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    local_datetime = serializers.SerializerMethodField()
    reply_content = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        [fields].append('category_name')
        [fields].append('user_name')
        [fields].append('local_datetime')
        [fields].append('reply_content')

    @staticmethod
    def get_category_name(obj):
        return obj.category.name

    @staticmethod
    def get_user_name(obj):
        return obj.user.username

    @staticmethod
    def get_local_datetime(obj):
        return l10n.localize(obj.changed_datetime)

    @staticmethod
    def get_reply_content(obj):
        return obj.reply_content
