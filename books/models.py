from django.db import models
from readme.models import User

# Create your models here.


class Book(models.Model):
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField()
    page_count = models.IntegerField()
    category = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    lang = models.CharField(max_length=2)


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(null=False, blank=False)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
