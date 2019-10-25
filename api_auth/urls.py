# -*- coding: utf-8 -*-
from django.conf.urls import url

from api_auth.views import LoginView, StatusView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^status/$', StatusView.as_view(), name='status'),
]
