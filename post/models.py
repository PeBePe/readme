from django.db import models
from readme.models import User
from books.models import Book

# Create your models here.


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post')
    book = models.ForeignKey(
        Book, on_delete=models.PROTECT, related_name='post')
    like_user = models.ManyToManyField(User, related_name='like_post')
