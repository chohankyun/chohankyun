# -*- coding: utf-8 -*-
from django.conf.urls import url

from api_auth.views import LoginView, StatusView, SessionUserView, UsernameFindView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^status/$', StatusView.as_view(), name='status'),
    url(r'^session/user/$', SessionUserView.as_view(), name='session_user'),
    url(r'^username/find/$', UsernameFindView.as_view(), name='username_find'),
    url(r'^password/reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/confirm/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<password>.+)/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password/change/$', PasswordChangeView.as_view(), name='password_change'),
]
