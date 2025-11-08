from django.contrib import admin
from .models import Book
# Register your models here.

admin.site.register(Book)

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # What columns appear in admin list
    search_fields = ("title", "author")                     # Enables search bar
    list_filter = ("publication_year",)                     # Adds filter sidebar on the right
