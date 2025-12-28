from django import forms
from .models import Post
from .models import Comment

# to handles create and update forms safely

class PostForm(forms.ModelForm):  #Modelform is explicity required, author will be automatiacally in view
    class Meta:
        model = Post
        fields = ["title", "content"]

        #users only type the comment text, post and author are set automatically in view
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
