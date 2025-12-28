from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200) #so this the title post, post database table
    content = models.TextField() # the full blog text
    published_date = models.DateTimeField(auto_now_add=True) #we used automatically set the post time we ltook for modls datetime field
    author = models.ForeignKey(User, on_delete=models.CASCADE) #it links the post to the user, why delete models gn

    def __str__(self):
        return self.title
