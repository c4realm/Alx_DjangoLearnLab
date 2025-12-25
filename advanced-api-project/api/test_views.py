# Tests for CRUD operations on Book API endpoints
# Includes GET, POST, PUT, DELETE

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author

class BookAPITests(APITestCase):
    def setUp(self):
        # Create an author for the books
        self.author = Author.objects.create(name="Test Author")

        # Create a book
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
    def test_get_books_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book(self):
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        url = reverse('book-update', args=[self.book.id])
        data = {'title': 'Updated Book', 'publication_year': 2023, 'author': self.author.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

