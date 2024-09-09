# Generated by Django 4.2.2 on 2024-08-09 08:55

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('libraryportal', '0004_borrowedbook'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowedbook',
            old_name='borrowed_date',
            new_name='borrowed_at',
        ),
        migrations.RemoveField(
            model_name='borrowedbook',
            name='book',
        ),
        migrations.RemoveField(
            model_name='borrowedbook',
            name='reader',
        ),
        migrations.AddField(
            model_name='borrowedbook',
            name='book_id',
            field=models.CharField(default=datetime.date(2024, 8, 9), max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='borrowedbook',
            name='book_title',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='borrowedbook',
            name='reference_id',
            field=models.CharField(default='unknown', max_length=100),
            preserve_default=False,
        ),
    ]