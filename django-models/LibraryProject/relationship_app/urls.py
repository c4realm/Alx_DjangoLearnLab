from django.urls import path
from .views import add_book, edit_book, delete_book

urlpatterns = [
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),
]

