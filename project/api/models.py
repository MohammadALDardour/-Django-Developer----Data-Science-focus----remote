from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)


    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Book, blank=True, related_name='favorited_by')

    def __str__(self):
        return self.user.username