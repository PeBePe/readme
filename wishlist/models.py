from django.db import models
from readme.models import User
from books.models import Book
# Create your models here.


class Wishlist(models.Model):
    wishlist_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='wishlist')
    books = models.ForeignKey(
        Book, on_delete=models.SET_NULL,  related_name='wishlist', null=True)