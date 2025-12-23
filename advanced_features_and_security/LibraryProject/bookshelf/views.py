"""
Secure views with proper imports and security decorators
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.utils.html import escape
import re
import os

from .models import Book, CustomUser
from .forms import BookForm, ExampleForm  # <-- This line must be exactly like this

# Rest of your views.py continues here...
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Role-based views from RBAC task
@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_view(request):
    return render(request, 'bookshelf/admin_view.html')

@user_passes_test(is_librarian, login_url='/accounts/login/')
def librarian_view(request):
    return render(request, 'bookshelf/librarian_view.html')

@user_passes_test(is_member, login_url='/accounts/login/')
def member_view(request):
    return render(request, 'bookshelf/member_view.html')


# Book views with permissions
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': 'Create Book'
    })

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': 'Edit Book',
        'book': book
    })

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


# Security-related views
def sanitize_input(input_string):
    if not input_string:
        return ""
    
    sanitized = str(input_string)
    sanitized = escape(sanitized)
    
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', '--']
    for keyword in sql_keywords:
        sanitized = re.sub(re.escape(keyword), '', sanitized, flags=re.IGNORECASE)
    
    return sanitized.strip()


@csrf_protect
def secure_search(request):
    results = []
    search_performed = False
    
    if request.method == 'GET':
        title = sanitize_input(request.GET.get('title', ''))
        author = sanitize_input(request.GET.get('author', ''))
        year = request.GET.get('year', '')
        
        try:
            year_int = int(year) if year else None
        except ValueError:
            year_int = None
        
        query = Book.objects.all()
        
        if title:
            query = query.filter(title__icontains=title)
        
        if author:
            query = query.filter(author__icontains=author)
        
        if year_int:
            query = query.filter(published_date__year__gte=year_int)
        
        results = query.order_by('title')[:50]
        search_performed = True
    
    return render(request, 'bookshelf/secure_search.html', {
        'results': results,
        'search_performed': search_performed,
    })


@csrf_protect
@permission_required('bookshelf.can_create', raise_exception=True)
def secure_book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        
        if form.is_valid():
            book = form.save(commit=False)
            
            isbn = form.cleaned_data.get('isbn', '')
            if not re.match(r'^\d{10}(\d{3})?$', isbn):
                form.add_error('isbn', 'ISBN must be 10 or 13 digits')
            
            from datetime import date
            if book.published_date and book.published_date > date.today():
                form.add_error('published_date', 'Publication date cannot be in the future')
            
            if not form.errors:
                book.save()
                messages.success(request, 'Book created securely!')
                return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/secure_book_form.html', {
        'form': form,
        'title': 'Create Book Securely'
    })


@csrf_protect
def add_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '')
        sanitized_comment = sanitize_input(comment_text)
        
        if len(sanitized_comment) < 5:
            messages.error(request, 'Comment must be at least 5 characters long.')
        elif len(sanitized_comment) > 500:
            messages.error(request, 'Comment cannot exceed 500 characters.')
        else:
            messages.success(request, 'Comment submitted securely!')
            import logging
            logger = logging.getLogger('django.security')
            logger.info(f'User {request.user.username} submitted a comment.')
        
        return redirect('form_example')
    
    return redirect('form_example')


def form_example(request):
    return render(request, 'bookshelf/form_example.html')


def display_user_input_safely(request):
    user_input = request.GET.get('input', '')
    safe_output_escaped = escape(user_input)
    safe_output_auto = user_input
    
    context = {
        'user_input': user_input,
        'safe_output': safe_output_auto,
        'dangerous_example': '<script>alert("XSS")</script>',
    }
    
    return render(request, 'bookshelf/safe_output.html', context)


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def security_audit(request):
    security_info = {
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        'CSRF_COOKIE_SECURE': settings.CSRF_COOKIE_SECURE,
        'SESSION_COOKIE_SECURE': settings.SESSION_COOKIE_SECURE,
        'SECURE_BROWSER_XSS_FILTER': settings.SECURE_BROWSER_XSS_FILTER,
        'X_FRAME_OPTIONS': settings.X_FRAME_OPTIONS,
        'SECURE_CONTENT_TYPE_NOSNIFF': settings.SECURE_CONTENT_TYPE_NOSNIFF,
        'SECURE_SSL_REDIRECT': settings.SECURE_SSL_REDIRECT,
        'SECURE_HSTS_SECONDS': settings.SECURE_HSTS_SECONDS,
        'PASSWORD_HASHERS': [h.split('.')[-1] for h in settings.PASSWORD_HASHERS],
    }
    
    return render(request, 'bookshelf/security_audit.html', {
        'security_info': security_info,
    })


@require_http_methods(["GET"])
def api_book_search(request):
    search_term = request.GET.get('q', '')
    
    if not search_term or len(search_term.strip()) < 2:
        return JsonResponse({'error': 'Search term must be at least 2 characters'}, status=400)
    
    if len(search_term) > 100:
        return JsonResponse({'error': 'Search term too long'}, status=400)
    
    books = Book.objects.filter(
        title__icontains=search_term
    ).values('id', 'title', 'author')[:10]
    
    book_list = list(books)
    
    return JsonResponse({'results': book_list}, safe=False)


def insecure_search_example(request):
    return render(request, 'bookshelf/insecure_example.html', {
        'warning': 'This is an example of what NOT to do!',
        'secure_alternative': 'Always use Django ORM or parameterized queries.',
    })


@csrf_protect
def example_form_view(request):
    message = ""
    form = ExampleForm()
    
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            age = form.cleaned_data['age']
            comment = form.cleaned_data.get('comment', '')
            
            import logging
            logger = logging.getLogger('django.security')
            logger.info(f'Form submitted by: {name}, Age: {age}')
            
            message = f"Thank you, {name}! Your form has been submitted securely."
            form = ExampleForm()
        else:
            message = "Please correct the errors below."
    
    return render(request, 'bookshelf/example_form.html', {
        'form': form,
        'message': message,
        'title': 'Secure Form Example'
    })


def form_security_demo(request):
    return render(request, 'bookshelf/form_security_demo.html')


