# -*- coding: utf-8 -*-
import copy

from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.views import ConfirmEmailView
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import Http404
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from rest_auth.serializers import PasswordResetConfirmSerializer, PasswordChangeSerializer
from rest_auth.views import LoginView, LogoutView
from rest_framework import status, exceptions
from rest_framework.generics import RetrieveAPIView, CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from auth_extend.serializers import PasswordResetExtendSerializer, UsernameFindSerializer, UserDetailsSerializer
from chohankyun import settings


class UserResetView(DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserDetailsSerializer

    def get_object(self):
        username = json.loads(self.request.body.decode('utf-8'))['username']
        password = json.loads(self.request.body.decode('utf-8'))['password']
        user = authenticate(username=username, password=password)

        if user and 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if email_address.verified:
                    raise exceptions.MethodNotAllowed()
        return user


class UserDetailsView(RetrieveUpdateDestroyAPIView, LogoutView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailsSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()

    def perform_update(self, serializer):
        before_user = copy.deepcopy(self.request.user)

        if not self.request.user.check_password(self.request.data['password']):
            raise exceptions.AuthenticationFailed(_('Invalid password.'))

        serializer.save()
        site = Site.objects.first()
        message_status = _('Your username has been updated from [%(before_username)s] to [%(current_username)s].') % (
            {'before_username': before_user.username, 'current_username': serializer.data['username']})
        message_solve = _('If your username is an invalid update, please update your username and password through username finding and Password finding on the login.')
        message = str(message_status) + '\r\n\r\n' + str(message_solve)
        send_mail('[' + site.name + '] ' + str(_('Your username has been updated.')), message, settings.DEFAULT_FROM_EMAIL, [before_user.email], fail_silently=False, )

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.check_password(json.loads(self.request.body.decode('utf-8'))['password']):
            raise exceptions.AuthenticationFailed(_('Invalid password.'))

        before_user = copy.deepcopy(self.request.user)

        instance = self.get_object()
        self.perform_destroy(instance)
        self.logout(request)

        site = Site.objects.first()
        message_status = _("All [%(before_username)s]'s information has been deleted. And all material related to [%(before_username)s] has been deleted.") % ({'before_username': before_user.username})
        message_solve = _('Thank you for using %(site_name)s [%(site_domain)s].') % ({'site_name': site.name, 'site_domain': site.domain})
        message = str(message_status) + '\r\n\r\n' + str(message_solve)
        send_mail('[' + site.name + '] ' + str(_('Your membership has been removed.')), message, settings.DEFAULT_FROM_EMAIL, [before_user.email], fail_silently=False, )

        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginExtendView(LoginView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = authenticate(username=self.request.data['username'], password=self.request.data['password'])

        if user:
            if user.is_staff:
                return Response({'non_field_errors': [_('You do not have permission to perform this action.')]}, status=status.HTTP_403_FORBIDDEN)

            if 'rest_auth.registration' in settings.INSTALLED_APPS:
                from allauth.account import app_settings
                if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                    email_address = user.emailaddress_set.get(email=user.email)
                    if not email_address.verified:
                        return Response({'non_field_errors': [_('E-mail is not verified.')]}, status=status.HTTP_406_NOT_ACCEPTABLE)

        return super(LoginExtendView, self).post(request, *args, **kwargs)


class UsernameFindView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UsernameFindSerializer

    def post(self, request):
        user = get_user_model().objects.filter(email=self.request.data['email']).first()
        if user is None:
            raise exceptions.ParseError(_('E-mail address matching query does not exist.'))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_('Your username has been sent to your e-mail address.'))


class PasswordResetView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetExtendSerializer

    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.filter(email=self.request.data['email']).first()
        if user is None:
            raise exceptions.ParseError(_('E-mail address matching query does not exist.'))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_('Password reset e-mail has been sent.'))


class PasswordResetConfirmView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def get(self, request, *args, **kwargs):
        data = self.kwargs
        data['new_password1'] = self.kwargs['password']
        data['new_password2'] = self.kwargs['password']
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError:
            return HttpResponse(_('Invalid value.'), status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return HttpResponse(_('Password has been reset with the new password.'))


class PasswordChangeView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError:
            if serializer.errors.get('old_password'):
                raise exceptions.AuthenticationFailed(_('Invalid old password.'))
            if serializer.errors.get('new_password2'):
                raise exceptions.AuthenticationFailed(_('The new password and the new password confirmation do not match.'))

        serializer.save()
        site = Site.objects.first()
        message_status = _('Your password has been updated from [%(old_password)s] to [%(new_password)s].') % (
            {'old_password': request.data['old_password'], 'new_password': request.data['new_password1']})
        message_solve = _('If your Password is an invalid update, please update your username and password through Password finding and Password finding on the login.')
        message = str(message_status) + '\r\n\r\n' + str(message_solve)
        send_mail('[' + site.name + '] ' + str(_('Your Password has been updated.')), message, settings.DEFAULT_FROM_EMAIL, [request.data['email']], fail_silently=False, )
        return Response(_('New password has been saved.'))


class ConfirmEmailExtendView(ConfirmEmailView):
    permission_classes = (AllowAny,)
    template_name = 'account/email_confirm.' + app_settings.TEMPLATE_EXTENSION
    object = None

    def get(self, *args, **kwargs):
        try:
            self.object = confirmation = self.get_object()
            confirmation.confirm(self.request)
            get_adapter(self.request).add_message(
                self.request, messages.SUCCESS, 'account/messages/email_confirmed.txt',
                {'e-mail': confirmation.email_address.email, 'user': confirmation.email_address.user})
        except Http404:
            super.object = None
        ctx = self.get_context_data()
        return self.render_to_response(ctx)
