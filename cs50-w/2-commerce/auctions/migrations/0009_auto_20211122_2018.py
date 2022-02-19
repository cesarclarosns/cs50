# Generated by Django 3.2.9 on 2021-11-22 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_category_auction_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='amount_currency',
        ),
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
