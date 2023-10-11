from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book


class User(AbstractUser):
    id = models.AutoField(primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    birthdate = models.DateField()
    biodata = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    loyalty_point = models.IntegerField(default=0)
    bookshelf = models.ManyToManyField(Book, related_name='bookshelf')
    shopping_cart = models.ManyToManyField(Book, related_name='shopping_cart')
