from django.urls import path
from . import views

urlpatterns = [
    path('Admin-view/', views.admin_view, name='Admin_view'),
    path('Librarian-view/', views.librarian_view, name='Librarian_view'),
    path('Member-view/', views.member_view, name='Member_view'),
]

