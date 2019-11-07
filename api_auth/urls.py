# -*- coding: utf-8 -*-
from django.conf.urls import url

from api_auth.views import (LoginView, StatusView, SessionUserView, UsernameFindView, PasswordResetView,
                            PasswordResetConfirmView, PasswordChangeView, RegisterView, EmailConfirmView,
                            UserResetView, SessionUserDeleteView, SessionUserUpdateView)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^status/$', StatusView.as_view(), name='status'),
    url(r'^session/user/$', SessionUserView.as_view(), name='session_user'),
    url(r'^username/find/$', UsernameFindView.as_view(), name='username_find'),
    url(r'^password/reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/confirm/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<password>.+)/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password/change/$', PasswordChangeView.as_view(), name='password_change'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^email/confirm/(?P<key>[-:\w]+)/$', EmailConfirmView.as_view(), name="email_confirm"),
    url(r'^user/reset/$', UserResetView.as_view(), name='user_reset'),
    url(r'^session/user/delete/$', SessionUserDeleteView.as_view(), name='session_user_delete'),
    url(r'^session/user/update/$', SessionUserUpdateView.as_view(), name='session_user_update'),
]
