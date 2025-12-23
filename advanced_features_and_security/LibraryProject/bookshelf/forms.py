"""
Form for Book model
"""
from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn', 'description']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'isbn': 'ISBN',
            'published_date': 'Published Date',
        }
    
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) not in [10, 13]:
            raise forms.ValidationError('ISBN must be 10 or 13 characters long')
        return isbn
