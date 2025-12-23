"""
Command to create and configure groups with permissions
Location: bookshelf/management/commands/setup_groups.py
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Creates and configures groups with permissions'

    def handle(self, *args, **options):
        # Get content type for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Get all permissions for Book model
        book_permissions = Permission.objects.filter(content_type=content_type)
        
        # Create groups and assign permissions
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
                    perm = book_permissions.get(codename=codename)
                    group.permissions.add(perm)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Added permission "{codename}" to group "{group_name}"'
                        )
                    )
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Permission "{codename}" not found for Book model'
                        )
                    )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Updated existing group: {group_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up all groups and permissions')
        )
