# Generated by Django 5.0.7 on 2024-08-09 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Listings',
            new_name='Listing',
        ),
    ]