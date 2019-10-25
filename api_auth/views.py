from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api_auth.serializers import LoginSerializer, JWTSerializer, SessionUserSerializer, UsernameFindSerializer

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
        serializer.is_valid(raise_exception=True)
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

