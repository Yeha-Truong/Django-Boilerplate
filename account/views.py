from django.contrib.auth import authenticate
from django.contrib.auth import signals as auth_signals
from django.utils import timezone
from knox import models as knox_models
from knox import views as knox_views
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from core import models as core_models
from core import serializers as core_serializers
from core import utils as core_utils
from account import serializers


class SignupView(generics.GenericAPIView):
    permission_classes = [~permissions.IsAuthenticated | permissions.IsAdminUser]
    serializer_class = serializers.UserSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.create(serializer.validated_data)
        return Response(
            core_utils.generateHttpResponse(
                data=core_serializers.UserSerializer(user).data,
                message="Your account have been registered successfully!",
            ),
            status=status.HTTP_201_CREATED,
        )


class SigninView(generics.GenericAPIView, knox_views.LoginView):
    permission_classes = [~permissions.IsAuthenticated | permissions.IsAdminUser]
    serializer_class = serializers.UserSigninSerializer

    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {"expiry": self.format_expiry_datetime(instance.expiry), "token": token}
        if UserSerializer is not None:
            data["user"] = UserSerializer(request.user, context=self.get_context()).data
        return data

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data, context=self.get_context())
        serializer.is_valid(raise_exception=True)
        user: core_models.User = authenticate(
            request=request, **serializer.validated_data
        )

        if user is not None:
            request.user = user

            isTokenAllocated = hasattr(user, "auth_token_set")
            token_limit_per_user = self.get_token_limit_per_user()
            if isTokenAllocated and token_limit_per_user is not None:
                now = timezone.now()
                token = user.auth_token_set.filter(expiry__gt=now)
                if token.count() >= token_limit_per_user:
                    return Response(
                        core_utils.generateHttpResponse(
                            error="Maximum amount of tokens allowed per user exceeded!",
                            message="Maximum amount of tokens allowed per user exceeded!",
                        ),
                        status=status.HTTP_403_FORBIDDEN,
                    )

            token_ttl = self.get_token_ttl()
            instance, token = knox_models.AuthToken.objects.create(
                request.user, token_ttl
            )
            auth_signals.user_logged_in.send(
                sender=request.user.__class__, request=request, user=request.user
            )
            data = self.get_post_response_data(request, token, instance)
            return Response(core_utils.generateHttpResponse(data=data))
        else:
            return Response(
                core_utils.generateHttpResponse(
                    error="Invalid credentials!", message="Invalid credentials!"
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignoutView(knox_views.LogoutView):
    permission_classes = [permissions.IsAuthenticated]


class InfoView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(core_serializers.UserSerializer(user).data)
