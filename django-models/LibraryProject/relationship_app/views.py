from django.shortcuts import render # i don't know what this is
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.http import HttpResponse


# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Library App!")


def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library",

