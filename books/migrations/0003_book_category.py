# Generated by Django 4.2.4 on 2023-10-23 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_isbn_book_page_count_book_publisher_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
