from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from users.models import User
from users.permissions import IsAccountUser
from .serializers import LoginSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class UserView(APIView):
    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


# class UserLogin(APIView):
#     def post(self, request: Request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = authenticate(
#             username=serializer.validated_data["username"],
#             password=serializer.validated_data["password"],
#         )
#         if user is None:
#             return Response(
#                 {"detail": "No active account found with the given credentials"},
#                 status.HTTP_401_UNAUTHORIZED,
#             )
#         refresh = RefreshToken.for_user(user)
#         token_data = {"access": str(refresh.access_token), "refresh": str(refresh)}
#         return Response(token_data, status.HTTP_200_OK)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountUser]

    def get(self, request: Request, user_id: int):
        found_user = get_object_or_404(User.objects.all(), pk=user_id)
        self.check_object_permissions(request, found_user)
        serializer = UserSerializer(found_user)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int):
        found_user = get_object_or_404(User.objects.all(), pk=user_id)
        self.check_object_permissions(request, found_user)
        serializer = UserSerializer(found_user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
