from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account as Master
from accounts.utils.tokens import user_auth_data

from .serializers import AccountPublicCreateSerializer, LoginWithCredentialsSerializer

###############################################################################
# Public
###############################################################################
class ApiPublicAccountCreate(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountPublicCreateSerializer
    model = Master

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)

        if data.is_valid():
            try:
                user = self.model.objects.create_user(
                    username=data.validated_data.get('username'),
                    email=data.validated_data.get('email'),
                    password=data.validated_data.get('password'),
                )
            except IntegrityError:
                return Response(
                    {
                        "details": "A user with this username or email already exists in the system!"
                    },
                    status=status.HTTP_409_CONFLICT
                )

            user_data = user_auth_data(user)

            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiLoginWithCredentials(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginWithCredentialsSerializer
    model = Master

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=request.data.get('email'),
            password=request.data.get('password')
        )

        if not user:
            return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)

        if not user.active:
            return Response({'detail': 'Account has been deactivated'}, status=status.HTTP_403_FORBIDDEN)

        user_data = user_auth_data(user)

        return Response(user_data, status=status.HTTP_200_OK)
