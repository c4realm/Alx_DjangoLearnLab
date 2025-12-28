from django import forms
from .models import Post

# to handles create and update forms safely

class PostForm(form.ModeForm):  #Modelform is explicity required, author will be automatiacally in view
    class Meta:
        model = Post
        fields = ["title", "content"]

