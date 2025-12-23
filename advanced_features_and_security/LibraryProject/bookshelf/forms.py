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

class ExampleForm(forms.Form):
    """
    Example form for demonstrating secure form handling.
    This form showcases various security practices:
    1. Input validation
    2. Length constraints
    3. Safe data handling
    4. CSRF protection (when used in templates)
    """
    # Example fields with validation
    name = forms.CharField(
        max_length=100,
        min_length=2,
        required=True,
        label='Full Name',
        help_text='Enter your full name (2-100 characters)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    
    email = forms.EmailField(
        max_length=150,
        required=True,
        label='Email Address',
        help_text='Enter a valid email address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@domain.com'
        })
    )
    
    age = forms.IntegerField(
        required=True,
        label='Age',
        min_value=1,
        max_value=120,
        help_text='Enter your age (1-120)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        })
    )
    
    comment = forms.CharField(
        required=False,
        label='Comment',
        max_length=500,
        help_text='Optional comment (max 500 characters)',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter your comment here...'
        })
    )
    
    agree_to_terms = forms.BooleanField(
        required=True,
        label='I agree to the terms and conditions',
        help_text='You must agree to proceed'
    )
    
    def clean_name(self):
        """Custom validation for name field"""
        name = self.cleaned_data.get('name', '').strip()
        
        # Security: Remove any HTML tags to prevent XSS
        import re
        name = re.sub(r'<[^>]*>', '', name)
        
        # Security: Remove SQL keywords
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', '--']
        for keyword in sql_keywords:
            if keyword.lower() in name.lower():
                raise forms.ValidationError(f'Invalid input detected')
        
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long')
        
        return name
    
    def clean_comment(self):
        """Custom validation for comment field"""
        comment = self.cleaned_data.get('comment', '').strip()
        
        # Security: Escape HTML entities
        import html
        comment = html.escape(comment)
        
        # Security: Limit length
        if len(comment) > 500:
            raise forms.ValidationError('Comment cannot exceed 500 characters')
        
        return comment
    
    def clean(self):
        """Form-wide validation"""
        cleaned_data = super().clean()
        
        # Example of cross-field validation
        age = cleaned_data.get('age')
        agree_to_terms = cleaned_data.get('agree_to_terms')
        
        if age and age < 18 and agree_to_terms:
            # Could add specific logic for minors
            pass
        
        return cleaned_data
