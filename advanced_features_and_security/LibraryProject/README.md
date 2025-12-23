# Django Permissions and Groups Management System

## Overview
This project implements a comprehensive permission-based access control system for managing books in a Django application. It demonstrates custom permissions, user groups, and permission enforcement in views.

## Features
- Custom permissions for Book model: `can_view`, `can_create`, `can_edit`, `can_delete`
- Predefined user groups: `Viewers`, `Editors`, `Admins`
- Permission enforcement using Django's `@permission_required` decorator
- Template-level permission checks
- Management command for automatic group setup

## Project Structure

LibraryProject/
├── bookshelf/ # Main application
│ ├── models.py # Custom User model & Book model with permissions
│ ├── views.py # Views with permission decorators
│ ├── admin.py # Admin configuration
│ ├── forms.py # Book forms
│ ├── urls.py # URL configurations
│ ├── management/commands/ # Custom management commands
│ │ └── setup_groups.py # Command to setup groups
│ └── templates/bookshelf/ # HTML templates
├── LibraryProject/ # Project settings
│ ├── settings.py # Django settings with AUTH_USER_MODEL
│ └── urls.py # Main URL configuration
└── README.md # This file
text


## Custom Permissions
The Book model defines four custom permissions in its Meta class:

```python
class Meta:
    permissions = [
        ("can_view", "Can view books"),
        ("can_create", "Can create books"),
        ("can_edit", "Can edit books"),
        ("can_delete", "Can delete books"),
    ]

User Groups

Three groups are configured with different permission levels:
1. Viewers

    Permissions: can_view

    Access: Can only view book listings and details

    Cannot: Create, edit, or delete books

2. Editors

    Permissions: can_view, can_create, can_edit

    Access: Can view, create, and edit books

    Cannot: Delete books

3. Admins

    Permissions: can_view, can_create, can_edit, can_delete

    Access: Full access to all book operations

Setup Instructions
1. Apply Migrations
bash

python manage.py makemigrations bookshelf
python manage.py migrate

2. Set Up Groups and Permissions
bash

python manage.py setup_groups

3. Create a Superuser (Optional)
bash

python manage.py createsuperuser

4. Run the Development Server
bash

python manage.py runserver

Testing the System
Manual Testing Commands

Run these commands in Django shell (python manage.py shell):
python

# Import necessary models
from django.contrib.auth.models import Group, Permission
from bookshelf.models import CustomUser, Book

# Check existing groups
print("Available groups:", [g.name for g in Group.objects.all()])

# Test user permissions
user = CustomUser.objects.get(username='your_username')
print(f"User: {user.username}")
print(f"Groups: {[g.name for g in user.groups.all()]}")
print(f"Can view: {user.has_perm('bookshelf.can_view')}")
print(f"Can create: {user.has_perm('bookshelf.can_create')}")
print(f"Can edit: {user.has_perm('bookshelf.can_edit')}")
print(f"Can delete: {user.has_perm('bookshelf.can_delete')}")

Test Users

After running the setup, these test users are available:
Username	Password	Group	Permissions
viewer_user	viewpass123	Viewers	View only
editor_user	editpass123	Editors	View, Create, Edit
admin_user	adminpass123	Admins	All permissions
Web Interface Testing

    Access the application: http://127.0.0.1:8000/books/

    Log in with different user accounts

    Test each user's capabilities:

        Viewers: Can only see the book list

        Editors: Can create and edit books, but not delete

        Admins: Can perform all actions including deletion

Views and Permission Enforcement

All views are protected with @permission_required decorators:
View	Permission Required	URL Pattern
Book List	can_view	/books/
Book Create	can_create	/books/create/
Book Detail	can_view	/books/<id>/
Book Edit	can_edit	/books/<id>/edit/
Book Delete	can_delete	/books/<id>/delete/
Template-Level Permission Checks

Templates include conditional rendering based on permissions:
html

{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}">Create New Book</a>
{% endif %}

{% if perms.bookshelf.can_edit %}
    <a href="{% url 'book_edit' book.pk %}">Edit</a>
{% endif %}

{% if perms.bookshelf.can_delete %}
    <a href="{% url 'book_delete' book.pk %}">Delete</a>
{% endif %}

Troubleshooting
Common Issues

    Permissions not working after migration

        Run python manage.py setup_groups to reset groups

        Clear browser cache and cookies

        Restart the development server

    Users can't access views

        Verify the user is assigned to the correct group

        Check that the group has the required permissions

        Ensure the user is logged in

    Template permission checks not working

        Make sure django.contrib.auth.context_processors.auth is in TEMPLATES.context_processors

        Verify the user has the required permissions

Debug Commands
bash

# Check all permissions in the system
python manage.py shell -c "from django.contrib.auth.models import Permission; print([p.codename for p in Permission.objects.filter(content_type__app_label='bookshelf')])"

# List all users and their groups
python manage.py shell -c "from bookshelf.models import CustomUser; for u in CustomUser.objects.all(): print(u.username, [g.name for g in u.groups.all()])"

Additional Resources

    Django Documentation: Authentication

    Django Documentation: Permissions

    Django Documentation: Groups

License

This project is for educational purposes as part of the ALX Django Learning Lab.
