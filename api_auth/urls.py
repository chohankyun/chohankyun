# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_auth.registration.views import VerifyEmailView

from api_auth.views import LoginView, StatusView
from auth_extend.views import PasswordResetConfirmView, PasswordResetView, UsernameFindView, UserDetailsView, PasswordChangeView, UserResetView

from auth_extend.views import (
    LoginExtendView,
    ConfirmEmailExtendView)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^status/$', StatusView.as_view(), name='status'),
]
