#!/usr/bin/env python
"""
Manual Testing Script for Permissions and Groups
Run this in Django shell or as a standalone script to test the setup
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book, CustomUser


def setup_test_users_and_groups():
    """
    Function to set up test users and groups for manual testing
    """
    print("Setting up test users and groups...")
    print("=" * 60)
    
    # Get content type for Book model
    content_type = ContentType.objects.get_for_model(Book)
    
    # Create groups with permissions
    groups_config = {
        'Viewers': ['can_view'],
        'Editors': ['can_view', 'can_create', 'can_edit'],
        'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
    }
    
    for group_name, perm_codenames in groups_config.items():
        group, created = Group.objects.get_or_create(name=group_name)
        group.permissions.clear()  # Clear any existing permissions
        
        for codename in perm_codenames:
            try:
                perm = Permission.objects.get(
                    content_type=content_type, 
                    codename=codename
                )
                group.permissions.add(perm)
                print(f"✓ Added '{codename}' permission to '{group_name}' group")
            except Permission.DoesNotExist:
                print(f"✗ Permission '{codename}' not found")
    
    print("\n" + "=" * 60)
    
    # Create test users
    test_users = [
        ('viewer_user', 'viewer@example.com', 'viewpass123', 'Viewers'),
        ('editor_user', 'editor@example.com', 'editpass123', 'Editors'),
        ('admin_user', 'admin@example.com', 'adminpass123', 'Admins'),
        ('regular_user', 'regular@example.com', 'regularpass123', None),  # No group
    ]
    
    for username, email, password, group_name in test_users:
        # Delete existing user if any
        CustomUser.objects.filter(username=username).delete()
        
        # Create new user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth='1990-01-01'
        )
        
        # Assign to group if specified
        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            print(f"✓ Created user '{username}' in '{group_name}' group")
        else:
            print(f"✓ Created user '{username}' (no group assignment)")
    
    print("\n" + "=" * 60)
    print("Test users created successfully!")
    print("\nLogin credentials:")
    print("Viewer: viewer_user / viewpass123")
    print("Editor: editor_user / editpass123")
    print("Admin: admin_user / adminpass123")
    print("Regular (no group): regular_user / regularpass123")
    print("\nRun 'python manage.py runserver' and test these accounts!")


def test_permissions():
    """
    Test if permissions are working correctly
    """
    print("\nTesting user permissions...")
    print("=" * 60)
    
    users = CustomUser.objects.filter(
        username__in=['viewer_user', 'editor_user', 'admin_user', 'regular_user']
    )
    
    for user in users:
        print(f"\nUser: {user.username}")
        print(f"Groups: {', '.join([g.name for g in user.groups.all()])}")
        
        permissions = [
            ('can_view', 'Can view'),
            ('can_create', 'Can create'),
            ('can_edit', 'Can edit'),
            ('can_delete', 'Can delete'),
        ]
        
        for perm_code, perm_name in permissions:
            has_perm = user.has_perm(f'bookshelf.{perm_code}')
            print(f"  {perm_name}: {'✓' if has_perm else '✗'}")


def create_test_book():
    """
    Create a test book for testing
    """
    # Delete any existing test book
    Book.objects.filter(title="Test Book").delete()
    
    # Create a test book
    book = Book.objects.create(
        title="Test Book",
        author="Test Author",
        published_date="2023-01-01",
        isbn="1234567890",
        description="A test book for permission testing"
    )
    print(f"\n✓ Created test book: '{book.title}'")
    return book


if __name__ == "__main__":
    print("PERMISSIONS AND GROUPS TEST SCRIPT")
    print("=" * 60)
    
    # Uncomment the functions you want to run
    setup_test_users_and_groups()
    test_permissions()
    create_test_book()
    
    print("\n" + "=" * 60)
    print("Setup complete! You can now:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/books/")
    print("3. Login with different users to test permissions")
