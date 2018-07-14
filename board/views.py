# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict

from bs4 import BeautifulSoup
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
    queryset = Category.objects.order_by('priority').all()
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
        if 'all' == self.kwargs.get('category'):
            return Post.objects.order_by('-%s' % self.kwargs.get('order')).all()
        return Post.objects.filter(category=self.kwargs.get('category')).order_by('-%s' % self.kwargs.get('order')).all()


class MyPostListByCategoryNOrder(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PostListPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        if 'all' == self.kwargs.get('category'):
            return Post.objects.filter(user=self.request.user.id).order_by('-%s' % self.kwargs.get('order')).all()
        return Post.objects.filter(user=self.request.user.id, category=self.kwargs.get('category')).order_by('-%s' % self.kwargs.get('order')).all()


class PostCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        obj_content = BeautifulSoup(request.data['content'], 'html.parser')
        request.data['text_content'] = obj_content.get_text()
        image = obj_content.img

        if image:
            request.data['first_image_source'] = image['src']
        else:
            request.data['first_image_source'] = ''

        return super(PostCreate, self).create(request, *args, **kwargs)


class PostUpdate(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def patch(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        obj_content = BeautifulSoup(request.data['content'], 'html.parser')
        request.data['text_content'] = obj_content.get_text()
        image = obj_content.img

        if image:
            request.data['first_image_source'] = image['src']
        else:
            request.data['first_image_source'] = ''

        return super(PostUpdate, self).partial_update(request, *args, **kwargs)


class PostDelete(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostIncreaseClickCount(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        count = Post.objects.filter(id=kwargs.get('pk')).values()[0].get('click_count')
        count = int(count) + 1
        increase_count = {'click_count': count}
        Post.objects.filter(id=kwargs.get('pk')).update(**increase_count)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        obj_content = BeautifulSoup(request.data['content'], 'html.parser')
        request.data['text_content'] = obj_content.get_text()
        return super(ReplyCreate, self).create(request, *args, **kwargs)

    def get_success_headers(self, data):
        post = Post.objects.get(pk=data.get('post'))
        post.reply_count = Reply.objects.filter(post=data.get('post')).count()
        post.save()
        return super(ReplyCreate, self).get_success_headers(data)


class ReplyList(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ReplySerializer

    def get_queryset(self):
        return Reply.objects.filter(post=self.kwargs.get('post_id')).order_by('-changed_datetime').all()


class ReplyUpdate(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def patch(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        obj_content = BeautifulSoup(request.data['content'], 'html.parser')
        request.data['text_content'] = obj_content.get_text()
        return super(ReplyUpdate, self).partial_update(request, *args, **kwargs)


class ReplyDelete(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        post = Post.objects.get(pk=instance.post.id)
        post.reply_count = Reply.objects.filter(post=instance.post.id).count()
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecommendCount(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        recommend_count = Recommend.objects.filter(post=self.kwargs.get('post_id')).count()
        recommend = Recommend.objects.filter(user=request.user.id, post=self.kwargs.get('post_id')).first()
        return Response({'recommend_count': recommend_count, 'is_recommend': True if recommend else False})


class RecommendCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super(RecommendCreate, self).create(request, *args, **kwargs)

    def get_success_headers(self, data):
        post = Post.objects.get(pk=data.get('post'))
        post.recommend_count = Recommend.objects.filter(post=data.get('post')).count()
        post.save()
        return super(RecommendCreate, self).get_success_headers(data)


class RecommendDelete(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = Recommend.objects.filter(user=request.user.id, post=self.kwargs.get('post_id')).first()
        self.perform_destroy(instance)
        post = Post.objects.get(pk=self.kwargs.get('post_id'))
        post.recommend_count = Recommend.objects.filter(post=self.kwargs.get('post_id')).count()
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
