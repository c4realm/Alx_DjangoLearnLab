#!/usr/bin/env python
"""
Test script to verify CustomUser model works correctly
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import CustomUser

print("Testing Custom User Model Implementation...")
print("=" * 50)

# Test 1: Create a regular user
try:
    user = CustomUser.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        date_of_birth='1995-05-15'
    )
    print(f"✓ Created regular user: {user.username}")
    print(f"  - Email: {user.email}")
    print(f"  - Date of birth: {user.date_of_birth}")
except Exception as e:
    print(f"✗ Failed to create regular user: {e}")
    sys.exit(1)

# Test 2: Create a superuser
try:
    superuser = CustomUser.objects.create_superuser(
        username='superuser',
        email='super@example.com',
        password='superpass123'
    )
    print(f"✓ Created superuser: {superuser.username}")
    print(f"  - Is staff: {superuser.is_staff}")
    print(f"  - Is superuser: {superuser.is_superuser}")
except Exception as e:
    print(f"✗ Failed to create superuser: {e}")
    sys.exit(1)

# Test 3: Verify AUTH_USER_MODEL setting
from django.conf import settings
print(f"✓ AUTH_USER_MODEL is set to: {settings.AUTH_USER_MODEL}")

print("=" * 50)
print("All tests passed! Custom User Model is working correctly.")
