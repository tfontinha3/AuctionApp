# Generated by Django 5.0.7 on 2024-08-09 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_listings_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='user_id',
            new_name='user',
        ),
    ]
