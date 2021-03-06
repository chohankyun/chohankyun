# -*- coding: utf-8 -*-
import logging
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from index .models import Header, Footer
from index.serializers import HeaderSerializer, FooterSerializer

logger = logging.getLogger(__name__)


class HeaderDetail(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = HeaderSerializer

    def get_object(self):
        return self.get_last_header_without_param()

    @staticmethod
    def get_last_header_without_param():
        return Header.objects.last()


class FooterDetail(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FooterSerializer

    def get_object(self):
        return self.get_last_footer_without_param()

    @staticmethod
    def get_last_footer_without_param():
        return Footer.objects.last()