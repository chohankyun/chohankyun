# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_auth.registration.views import VerifyEmailView
from auth_extend.views import PasswordResetConfirmView, PasswordResetView, UsernameFindView, UserDetailsView, PasswordChangeView, UserResetView

from auth_extend.views import (
    LoginExtendView,
    ConfirmEmailExtendView)

urlpatterns = [
    url(r'^user/reset/$', UserResetView.as_view(), name='rest_user_reset'),
    url(r'^user/$', UserDetailsView.as_view(), name='rest_user_details'),
    url(r'^login/$', LoginExtendView.as_view(), name='rest_login'),
    url(r'^username/find/$', UsernameFindView.as_view(), name='rest_username_find'),
    url(r'^password/reset/$', PasswordResetView.as_view(), name='rest_password_reset'),
    url(r'^password/reset/confirm/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<password>\w+)/$', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    url(r'^password/change/$', PasswordChangeView.as_view(), name='rest_password_change'),
    url(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailExtendView.as_view(), name="account_confirm_email"),
    url(r'^registration/account-email-verification-sent/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    url(r'^registration/', include('rest_auth.registration.urls')),
]
