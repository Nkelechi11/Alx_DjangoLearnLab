from django.shortcuts import render
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to anyone.
    Only allow object owners to edit or delete.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE methods are read-only (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for owner
        return obj.author == request.user


# 
from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from rest_framework import filters


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# view for follow and unfollow feed
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics, status


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def user_feed(request):
#     followed_users = request.user.following.all()

#     posts = Post.objects.filter(
#         author__in=followed_users
#     ).order_by("-created_at")

#     serializer = PostSerializer(posts, many=True)

#     return Response(serializer.data, status=status.HTTP_200_OK)

class UserFeedView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        followed_users = request.user.following.all()

        posts = Post.objects.filter(
            author__in=followed_users
        ).order_by("-created_at")

        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)