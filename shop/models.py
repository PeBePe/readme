from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class ShopItem(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    price = models.IntegerField()
