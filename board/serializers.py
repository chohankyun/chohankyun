# -*- coding: utf-8 -*-
from django.templatetags import l10n
from rest_framework import serializers
from board.models import Category, Post, Reply, Recommend


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    local_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        [fields].append('category_name')
        [fields].append('username')
        [fields].append('local_datetime')

    @staticmethod
    def get_category_name(obj):
        return obj.category.name

    @staticmethod
    def get_username(obj):
        return obj.user.username

    @staticmethod
    def get_local_datetime(obj):
        return l10n.localize(obj.updated_datetime)


class ReplySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    local_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = '__all__'
        [fields].append('username')
        [fields].append('local_datetime')

    @staticmethod
    def get_username(obj):
        return obj.user.username

    @staticmethod
    def get_local_datetime(obj):
        return l10n.localize(obj.updated_datetime)


class RecommendSerializer(serializers.ModelSerializer):
    recommend_count = serializers.SerializerMethodField()

    class Meta:
        model = Recommend
        fields = '__all__'
        [fields].append('recommend_count')

    @staticmethod
    def get_recommend_count(obj):
        return Recommend.objects.filter(post=obj.post).count()
