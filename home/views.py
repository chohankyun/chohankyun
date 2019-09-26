# -*- coding: utf-8 -*-
import logging
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from board.models import Post
from board.serializers import PostSerializer
from home.models import Carousel
from home.serializers import CarouselSerializer

logger = logging.getLogger(__name__)


class CarouselList(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CarouselSerializer

    def get_queryset(self):
        return self.get_three_carousel_by_priority()

    @staticmethod
    def get_three_carousel_by_priority():
        queryset = Carousel.objects.filter(priority__in=[1, 2, 3])
        queryset = queryset.order_by('priority')
        return queryset


class PostListByOrder(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.get_four_post_by_order()

    def get_four_post_by_order(self):
        queryset = Post.objects.order_by('-%s' % self.kwargs.get('order'))
        queryset = queryset[:4]
        return queryset


class MyPostListByOrder(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.get_four_post_by_user_and_order()

    def get_four_post_by_user_and_order(self):
        queryset = Post.objects.filter(user=self.request.user.id)
        queryset = queryset.order_by('-%s' % self.kwargs.get('order'))
        queryset = queryset[:4]
        return queryset
