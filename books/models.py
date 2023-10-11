from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    lang = models.CharField(max_length=10)
    image_url = models.CharField(max_length=255)
    publication_date = models.DateField()
