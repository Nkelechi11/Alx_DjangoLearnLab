from django.db import models

# Create your models here.
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

# relationship_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    def __str__(self):
        return f"{self.user.username} - {self.role}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# relationship_app/views.py

from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile


def is_admin(user):
    return user.is_authenticated and user.userprofile.role == "Admin"


def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == "Librarian"


def is_member(user):
    return user.is_authenticated and user.userprofile.role == "Member"


@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse("Welcome to the Admin view.")


@user_passes_test(is_librarian)
def librarian_view(request):
    return HttpResponse("Welcome to the Librarian view.")


@user_passes_test(is_member)
def member_view(request):
    return HttpResponse("Welcome to the Member view.")