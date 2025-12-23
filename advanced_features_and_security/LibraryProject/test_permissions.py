#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book, CustomUser

print("Testing Permissions and Groups Setup...")
print("=" * 60)

# Get content type for Book model
content_type = ContentType.objects.get_for_model(Book)

# Create groups if they don't exist
groups_config = {
    'Viewers': ['can_view'],
    'Editors': ['can_view', 'can_create', 'can_edit'],
    'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
}

for group_name, perm_codenames in groups_config.items():
    group, created = Group.objects.get_or_create(name=group_name)
    
    # Clear existing permissions
    group.permissions.clear()
    
    # Add new permissions
    for codename in perm_codenames:
        try:
            perm = Permission.objects.get(content_type=content_type, codename=codename)
            group.permissions.add(perm)
            print(f"✓ Added '{codename}' to '{group_name}' group")
        except Permission.DoesNotExist:
            print(f"✗ Permission '{codename}' not found")

# Create test users
test_users = [
    ('viewer_user', 'viewer@example.com', 'viewpass123', 'Viewers'),
    ('editor_user', 'editor@example.com', 'editpass123', 'Editors'),
    ('admin_user', 'admin@example.com', 'adminpass123', 'Admins'),
]

for username, email, password, group_name in test_users:
    # Check if user exists
    if not CustomUser.objects.filter(username=username).exists():
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth='1990-01-01'
        )
        
        # Assign to group
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        
        print(f"✓ Created user '{username}' in '{group_name}' group")
        
        # Test permissions
        print(f"  Permissions for {username}:")
        for perm_codename in ['can_view', 'can_create', 'can_edit', 'can_delete']:
            has_perm = user.has_perm(f'bookshelf.{perm_codename}')
            print(f"    - {perm_codename}: {has_perm}")
    else:
        print(f"⚠ User '{username}' already exists")

print("\n" + "=" * 60)
print("Testing Complete!")
print("\nLogin credentials:")
print("Viewer: viewer_user / viewpass123")
print("Editor: editor_user / editpass123")
print("Admin: admin_user / adminpass123")
