from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import User as CustomUser


# ------------------------
# Register View
# ------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(username=response.data["username"])
        token = Token.objects.get(user=user)

        return Response(
            {
                "user": response.data,
                "token": token.key
            },
            status=status.HTTP_201_CREATED
        )


# ------------------------
# Login View
# ------------------------
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# ------------------------
# Profile View
# ------------------------
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ------------------------
# Follow a User
# ------------------------
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)

        if request.user == user_to_follow:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_to_follow in request.user.following.all():
            return Response(
                {"message": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(user_to_follow)

        return Response(
            {"message": f"You are now following {user_to_follow.username}."},
            status=status.HTTP_200_OK
        )


# ------------------------
# Unfollow a User
# ------------------------
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

        if user_to_unfollow not in request.user.following.all():
            return Response(
                {"message": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.remove(user_to_unfollow)

        return Response(
            {"message": f"You have unfollowed {user_to_unfollow.username}."},
            status=status.HTTP_200_OK
        )


# ------------------------
# List All Users
# ------------------------
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]