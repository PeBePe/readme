from django.db import models

# Create your models here.


class Quote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quote = models.TextField()
