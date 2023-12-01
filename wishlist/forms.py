from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from books.models import Book
from django.forms import ModelForm
from wishlist.models import Wishlist

class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = ('note', 'user', 'books')