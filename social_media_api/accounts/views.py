from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
# creating follow and unfollow endpoints
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import User


# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.serializer_class.Meta.model.objects.get(username=response.data['username'])
        token = Token.objects.get(user=user)
        return Response({
            'user': response.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

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

# everything above is about project setup and custom user model creation

# creating endpoints for follow and unfollow


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)

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