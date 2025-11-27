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
           #djangos built in login system, LoginViewas_view(template_name = the directory named as the same as app name because django demands it in the file login. html
        path('login/', LoginView.as_view(template_name="relationship_app/login.html"), name='login'),
        path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), name='logout'),
        path('register/', views.register, name='register'),
        
        ]

