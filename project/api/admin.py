from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book, Author, UserProfile


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(UserProfile)