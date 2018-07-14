# -*- coding: utf-8 -*-
from django.conf.urls import url
from index.views import HeaderDetail ,FooterDetail

urlpatterns = [
    url(r'^header/detail/$', HeaderDetail.as_view(), name='header_detail'),
    url(r'^footer/detail/$', FooterDetail.as_view(), name='footer_detail'),
]
