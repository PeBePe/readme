from django.db import models
from readme.models import User

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    lang = models.CharField(max_length=10)
    image_url = models.CharField(max_length=255)
    publication_date = models.DateField()


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(null=False, blank=False)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
