# Generated by Django 5.0.7 on 2024-08-25 20:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_watchlist_listings_alter_watchlist_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
