"""
URLs for bookshelf app
"""
from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
]

# Example form URL
path('example-form/', views.example_form_view, name='example_form'),
path('form-security/', views.form_security_demo, name='form_security_demo'),
