from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    published_date = models.DateField()

    class Meta:
        permissions = (
            ("canaddbook", "Can add book"),
            ("canchangebook", "Can change book"),
            ("candeletebook", "Can delete book"),
        )

    def __str__(self):
        return self.title

