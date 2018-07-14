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
    queryset = Carousel.objects.filter(priority__in=[1, 2, 3]).order_by('priority').all()
    serializer_class = CarouselSerializer


class PostListByOrder(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    # 홈 값은 각 카테코리 별로 4개만 조회 합니다.
    def get_queryset(self):
        return Post.objects.order_by('-%s' % self.kwargs.get('order')).all()[:4]


class MyPostListByOrder(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user.id).order_by('-%s' % self.kwargs.get('order')).all()[:4]
