from django.urls import path
from .views import BookListCreateView, BookDetailView, AuthorListCreateView, AuthorDetailView, register, login, add_to_favorites, remove_from_favorites, recommended_books


urlpatterns = [
    # Book endpoints
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:id>/', BookDetailView.as_view(), name='book-detail'),

    # Author endpoints
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:id>/', AuthorDetailView.as_view(), name='author-detail'),

    # User authentication
    path('register/', register, name='register'),
    path('login/', login, name='login'),

    # Favorites and recommendations
    path('favorites/add/<int:book_id>/', add_to_favorites, name='add-to-favorites'),
    path('favorites/remove/<int:book_id>/', remove_from_favorites, name='remove-from-favorites'),
    path('recommendations/', recommended_books, name='recommended-books'),
]