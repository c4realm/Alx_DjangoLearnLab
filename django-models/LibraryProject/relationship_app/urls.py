from django.contrib import admin
from django.urls import path
from .views import list_books
from . import views
from .views import list_books, user_login, user_logout, register, LibraryDetailView


urlpatterns = [
        path("", user_login, name="home"),
        path("books/", list_books, name = "list_books"),
        path("library/<int:pk>/", views.LibraryDetailView.as_view(), name = "library_detail"),  
           # NEW AUTH URLS
        path("login/", user_login, name="login"),
        path("logout/", user_logout, name="logout"),
        path("register/", register, name="register"),
        
        ]

