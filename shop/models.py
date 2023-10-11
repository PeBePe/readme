from django.db import models
from django.core.validators import MinValueValidator
from books.models import Book

# Create your models here.


class ShopItem(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    price = models.IntegerField()
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, related_name='shop_item')
