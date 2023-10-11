from django.db import models
from readme.models import User
# Create your models here.


class Wishlist(models.Model):
    wishlist_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField()
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
