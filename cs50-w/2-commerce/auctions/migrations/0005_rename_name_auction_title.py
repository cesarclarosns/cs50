# Generated by Django 3.2.7 on 2021-11-11 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auction_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='name',
            new_name='title',
        ),
    ]