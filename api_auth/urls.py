# -*- coding: utf-8 -*-
from django.conf.urls import url

from api_auth.views import LoginView, StatusView, SessionUserView, UsernameFindView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^status/$', StatusView.as_view(), name='status'),
    url(r'^session/user/$', SessionUserView.as_view(), name='session_user'),
    url(r'^username/find/$', UsernameFindView.as_view(), name='username_find'),
]
