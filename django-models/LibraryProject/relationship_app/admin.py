from django.contrib import admin
# from .models import Book  # Comment this out if Book doesn't exist
from .models import UserProfile  # Add this

# admin.site.register(Book)  # Comment this out
admin.site.register(UserProfile)  # Add this
