# relationship_app/urls.py

from django.urls import path
from .views import list_books, LibraryDetailView

app_name = "relationship_app"

# urlpatterns = [
#     # Function-based view URL
#     path("books/", list_books, name="list_books"),
    
#     # Class-based view URL
#     path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
# ]
# after implementing user authentication

# from django.urls import path
from .views import (
    # list_books,
    # LibraryDetailView,
    RegisterView,
    UserLoginView,
    UserLogoutView,
)
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = "relationship_app"

urlpatterns = [
    # Function-based view
    path("books/", list_books, name="list_books"),

    # Class-based view
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Authentication URLs
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),

    # Authentication- alternative
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

]