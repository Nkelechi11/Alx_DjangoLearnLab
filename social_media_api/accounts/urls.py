from django.urls import path
from .views import RegisterView, LoginView, ProfileView, follow_user, unfollow_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # everything above is about project setup and custom user model creation
    # urls for follow and unfollow endpoints
    path("follow/<int:user_id>/", follow_user, name="follow-user"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow-user"),
]

