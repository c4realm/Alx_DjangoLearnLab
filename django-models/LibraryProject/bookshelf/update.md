from bookshelf.models import Book

book = Book.objects.first()
book.title = "Nineteen Eighty-Four"
book.save()
book
# <Book: Nineteen Eighty-Four by George Orwell>
