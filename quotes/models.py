from django.db import models
from readme.models import User

# Create your models here.


class Quote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quote = models.TextField()
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='quote')
    citing_user = models.ManyToManyField(User, related_name='citing_quote')
