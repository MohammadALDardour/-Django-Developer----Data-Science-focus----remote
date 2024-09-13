from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Book, Author, UserProfile
from .serializers import BookSerializer, AuthorSerializer, UserProfileSerializer


# Book Views
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# Author Views
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# User Registration
@api_view(['POST'])
def register(request):
    username = request.data['username']
    password = request.data['password']
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


# User Login
@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    user = User.objects.get(username=username)
    if user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Add/Remove Favorites
@api_view(['POST'])
def add_to_favorites(request, book_id):
    book = Book.objects.get(id=book_id)
    profile = UserProfile.objects.get(user=request.user)
    profile.favorites.add(book)
    profile.save()
    return Response({'message': 'Added to favorites'})


@api_view(['POST'])
def remove_from_favorites(request, book_id):
    book = Book.objects.get(id=book_id)
    profile = UserProfile.objects.get(user=request.user)
    profile.favorites.remove(book)
    profile.save()
    return Response({'message': 'Removed from favorites'})


# Recommendation System
@api_view(['GET'])
def recommended_books(request):
    profile = UserProfile.objects.get(user=request.user)
    favorite_books = profile.favorites.all()
    recommended_books = Book.objects.exclude(id__in=favorite_books.values_list('id', flat=True))[:5]
    serializer = BookSerializer(recommended_books, many=True)
    return Response(serializer.data)


def get_queryset(self):
    queryset = Book.objects.all()
    search = self.request.query_params.get('search')
    if search:
        queryset = queryset.filter(title__icontains=search) | queryset.filter(author__name__icontains=search)
    return queryset