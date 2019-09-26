# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict

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
        search_word = self.get_search_word()
        return self.get_post_by_search_word(search_word)

    def get_search_word(self):
        search_word = self.kwargs.get('search_word')

        if not search_word:
            raise exceptions.ParseError(_('Please enter at least 2 characters.'))
        if len(search_word) < 2:
            raise exceptions.ParseError(_('Please enter at least 2 characters.'))

        return search_word

    def get_post_by_search_word(self, search_word):
        queryset = Post.objects.filter(
            Q(subject__icontains=search_word) |
            Q(text_content__icontains=search_word) |
            Q(reply__text_content__icontains=search_word))

        queryset = queryset.order_by('-%s' % self.kwargs.get('order'))
        queryset = queryset.annotate(reply_content=F('reply__content'))
        return queryset
