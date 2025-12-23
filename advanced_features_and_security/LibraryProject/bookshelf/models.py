"""
Custom User Model Implementation
Location: advanced_features_and_security/LibraryProject/relationship_app/models.py
Purpose: Replace Django's default User model with custom one
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model
    Required by the task: create_user and create_superuser methods
    """
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given username, email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given username, email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser
    Required fields by the task:
    1. date_of_birth: A date field
    2. profile_photo: An image field
    """
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # Use the custom manager
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username

class Book(models.Model):
    """
    Book model with custom permissions
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        # Custom permissions as specified in the task
        permissions = [
            ("can_view", "Can view books"),
            ("can_create", "Can create books"),
            ("can_edit", "Can edit books"),
            ("can_delete", "Can delete books"),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author}"
