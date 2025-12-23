"""
Custom User Admin Configuration
Location: advanced_features_and_security/LibraryProject/relationship_app/admin.py
Purpose: Modify Django admin to support the custom user model
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for CustomUser model
    Required by the task: custom ModelAdmin class with additional fields
    """
    model = CustomUser
    
    # Fields to display in the admin list view
    list_display = ('username', 'email', 'date_of_birth', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Fieldsets for the edit form - includes new fields
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldsets for the add form - includes new fields
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'date_of_birth'),
        }),
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
