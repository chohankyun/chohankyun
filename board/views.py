# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict

from bs4 import BeautifulSoup
from django.db.models import F
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from board.models import Category, Post, Reply, Recommend
from board.serializers import CategorySerializer, PostSerializer, ReplySerializer, RecommendSerializer

logger = logging.getLogger(__name__)


class CategoryList(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Category.objects.order_by('priority')
    serializer_class = CategorySerializer


class PostDetail(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostListPagination(PageNumberPagination):
    page_size = 16

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page', self.page.number),
            ('total', self.page.paginator.count),
            ('page_size', self.page_size),
            ('results', data)
        ]))


class PostListByCategoryNOrder(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PostListPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.get_post_by_category_and_order()

    def get_post_by_category_and_order(self):
        queryset = Post.objects.order_by('-%s' % self.kwargs.get('order'))
        if 'all' != self.kwargs.get('category'):
            queryset = queryset.filter(category=self.kwargs.get('category'))
        return queryset


class MyPostListByCategoryNOrder(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PostListPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.get_my_post_by_category_and_order()

    def get_my_post_by_category_and_order(self):
        queryset = Post.objects.filter(user=self.request.user.id)
        queryset = queryset.order_by('-%s' % self.kwargs.get('order'))
        if 'all' != self.kwargs.get('category'):
            queryset.filter(category=self.kwargs.get('category'))
        return queryset


class HtmlContent:
    @staticmethod
    def add_content(request):
        obj_content = BeautifulSoup(request.data['content'], 'html.parser')
        request.data['text_content'] = obj_content.get_text()
        return request

    @staticmethod
    def add_content_with_image(request):
        obj_content = BeautifulSoup(request.data['content'], 'html.parser')
        request.data['text_content'] = obj_content.get_text()
        image = obj_content.img
        request.data['first_image_source'] = image['src'] if image else ''
        return request


class PostCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request = HtmlContent.add_content_with_image(request)
        return super(PostCreate, self).create(request, *args, **kwargs)


class PostUpdate(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def patch(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request = HtmlContent.add_content_with_image(request)
        return super(PostUpdate, self).partial_update(request, *args, **kwargs)


class PostDelete(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostIncreaseClickCount(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        self.increase_click_count()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def increase_click_count(self):
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        post.click_count = F('click_count') + 1
        post.save()


class ReplyCount:
    @staticmethod
    def save(post_id):
        post = Post.objects.get(pk=post_id)
        post.reply_count = Reply.objects.filter(post=post_id).count()
        post.save()


class ReplyCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request = HtmlContent.add_content(request)
        return super(ReplyCreate, self).create(request, *args, **kwargs)

    def get_success_headers(self, data):
        ReplyCount.save(data.get('post'))
        return super(ReplyCreate, self).get_success_headers(data)


class ReplyList(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ReplySerializer

    def get_queryset(self):
        return self.get_reply_by_post()

    def get_reply_by_post(self):
        queryset = Reply.objects.filter(post=self.kwargs.get('post_id'))
        queryset = queryset.order_by('-changed_datetime')
        return queryset


class ReplyUpdate(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def patch(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request = HtmlContent.add_content(request)
        return super(ReplyUpdate, self).partial_update(request, *args, **kwargs)


class ReplyDelete(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        ReplyCount.save(instance.post.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecommendCount:
    @staticmethod
    def save(post_id):
        post = Post.objects.get(pk=post_id)
        post.recommend_count = Recommend.objects.filter(post=post_id).count()
        post.save()


class RecommendCountNOwner(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        queryset = Recommend.objects.filter(post=self.kwargs.get('post_id'))
        recommend_count = queryset.count()
        is_recommend = queryset.filter(user=request.user.id).exists()
        return Response({'recommend_count': recommend_count, 'is_recommend': is_recommend})


class RecommendCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super(RecommendCreate, self).create(request, *args, **kwargs)

    def get_success_headers(self, data):
        RecommendCount.save(data.get('post'))
        return super(RecommendCreate, self).get_success_headers(data)


class RecommendDelete(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        queryset = Recommend.objects.filter(user=request.user.id)
        queryset = queryset.filter(post=self.kwargs.get('post_id'))
        instance = queryset.first()
        self.perform_destroy(instance)
        RecommendCount.save(self.kwargs.get('post_id'))
        return Response(status=status.HTTP_204_NO_CONTENT)
