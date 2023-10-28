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


class Bookshelf(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='bookshelf')


class BookshelfItem(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)
    item = models.ForeignKey(
        ShopItem, on_delete=models.SET_NULL, null=True, related_name='bookshelves')
    bookshelf = models.ForeignKey(
        Bookshelf, on_delete=models.CASCADE, related_name='books')


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='shopping_cart')


class ShoppingCartItem(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)
    item = models.ForeignKey(
        ShopItem, on_delete=models.CASCADE, related_name='shopping_carts')
    shopping_cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, related_name='books')
