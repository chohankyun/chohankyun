# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict
import urllib.parse

from django.utils.translation import ugettext_lazy as _
from django.db.models import Q, F
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import exceptions


from board.models import Post
from search.serializers import SearchSerializer

logger = logging.getLogger(__name__)


class SearchListPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page', self.page.number),
            ('total', self.page.paginator.count),
            ('page_size', self.page_size),
            ('results', data)
        ]))


class SearchPostByOrder(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = SearchListPagination
    serializer_class = SearchSerializer

    def get_queryset(self):
        if self.kwargs.get('search_word') is None:
            raise exceptions.ParseError(_('Please enter at least 2 characters.'))

        if self.kwargs.get('search_word') == "":
            raise exceptions.ParseError(_('Please enter at least 2 characters.'))

        logger.info("before decode:"+self.kwargs.get('search_word'))
        search_word = urllib.parse.unquote(self.kwargs.get('search_word'))
        logger.info("after decode:" + self.kwargs.get('search_word'))

        if len(search_word) < 2:
            raise exceptions.ParseError(_('Please enter at least 2 characters.'))

        return Post.objects.filter(
            Q(subject__contains=search_word) |
            Q(text_content__contains=search_word) |
            Q(reply__text_content__contains=search_word)
        ).order_by('-%s' % self.kwargs.get('order')).all().annotate(reply_content=F('reply__content'))
