import json

from django.contrib.auth import get_user_model, user_logged_in
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status, exceptions
from rest_framework.generics import GenericAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api_auth.serializers import (LoginSerializer, JWTSerializer, SessionUserSerializer, UsernameFindSerializer,
                                  PasswordResetSerializer, PasswordResetConfirmSerializer, PasswordChangeSerializer,
                                  RegisterSerializer, EmailConfirmSerializer)

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def post(self, request):
        user = self.login(request)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return self.get_response(user)

    def login(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data['user']

    def get_response(self, user):
        jwt_serializer = JWTSerializer(instance=user, context={'request': self.request})
        return Response(jwt_serializer.data, status=status.HTTP_200_OK)


class StatusView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JWTSerializer

    def get(self, request):
        serializer = self.get_serializer(instance=request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SessionUserView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SessionUserSerializer

    def get_object(self):
        user_id = self.request.user.id
        return get_user_model().objects.get(pk=user_id)


class UsernameFindView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UsernameFindSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_('Your username has been sent to your e-mail address.'))


class PasswordResetView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_('Password reset e-mail has been sent.'))


class PasswordResetConfirmView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def get(self, request, **kwargs):
        try:
            serializer = self.get_serializer(data=kwargs, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except exceptions.ValidationError as e:
            return HttpResponse(e.default_detail, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(_('Password has been reset with the new password.'))


class PasswordChangeView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_('Password has been changed with the new password.'))


class RegisterView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_('Verification email sent.'))


class EmailConfirmView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailConfirmSerializer

    def get(self, request, **kwargs):
        try:
            serializer = self.get_serializer(data=kwargs, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except exceptions.ValidationError as e:
            return HttpResponse(e.default_detail, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(_('Your email has been verified.'))


class UserResetView(DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def get_object(self):
        username = json.loads(self.request.body.decode('utf-8'))['username']
        password = json.loads(self.request.body.decode('utf-8'))['password']
        serializer = self.get_serializer(context={'request': self.request})
        return serializer.authenticate(username=username, password=password)


class SessionUserDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user_id = self.request.user.id
        return get_user_model().objects.get(pk=user_id)

    def perform_destroy(self, instance):
        if not instance.check_password(self.request.body.decode('utf-8')):
            raise exceptions.AuthenticationFailed(_('Invalid password.'))
        instance.delete()


class SessionUserUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SessionUserSerializer

    def get_object(self):
        user_id = self.request.user.id
        return get_user_model().objects.get(pk=user_id)

    def perform_update(self, serializer):
        if not serializer.instance.check_password(self.request.data['password']):
            raise exceptions.AuthenticationFailed(_('Invalid password.'))
        serializer.save()
