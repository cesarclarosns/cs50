# Generated by Django 3.2.9 on 2021-12-26 02:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20211226_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='reactions',
        ),
        migrations.AddField(
            model_name='post',
            name='reacted',
            field=models.ManyToManyField(related_name='reactions', to=settings.AUTH_USER_MODEL),
        ),
    ]
