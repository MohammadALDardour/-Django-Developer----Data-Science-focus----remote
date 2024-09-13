from rest_framework import serializers
from .models import Book, Author, UserProfile


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    favorites = BookSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'favorites']