from django.db import models
from readme.models import User


class Quote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quote = models.TextField()
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='quote')


class QuoteCited(models.Model):
    cited_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cited_quote')
    quote_id = models.ForeignKey(
        Quote, on_delete=models.CASCADE, related_name='cited_quote')
