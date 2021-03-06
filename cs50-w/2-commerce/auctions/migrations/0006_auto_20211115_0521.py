# Generated by Django 3.2.7 on 2021-11-15 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_name_auction_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='bid',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='user',
            name='auction',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bid',
        ),
        migrations.RemoveField(
            model_name='user',
            name='comment',
        ),
        migrations.AddField(
            model_name='auction',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auction'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='auction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auction'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='auction',
            name='category',
        ),
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.ManyToManyField(null=True, related_name='categories', to='auctions.Category'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('USD', 'US Dollar')], default='XYZ', editable=False, max_length=3),
        ),
    ]
