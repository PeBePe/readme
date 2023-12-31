from django.db import models
from django.core.validators import MinValueValidator
from books.models import Book
from readme.models import User
# Create your models here.


class ShopItem(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    price = models.IntegerField()
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, related_name='shop_item')


class BookshelfItem(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)
    item = models.ForeignKey(
        ShopItem, on_delete=models.SET_NULL, null=True, related_name='bookshelf')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookshelf')


class ShoppingCartItem(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)
    item = models.ForeignKey(
        ShopItem, on_delete=models.CASCADE, related_name='shopping_cart')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart')
