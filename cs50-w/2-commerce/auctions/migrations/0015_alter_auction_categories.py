# Generated by Django 3.2.9 on 2021-11-27 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_auction_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='categories',
            field=models.ManyToManyField(to='auctions.Category'),
        ),
    ]
