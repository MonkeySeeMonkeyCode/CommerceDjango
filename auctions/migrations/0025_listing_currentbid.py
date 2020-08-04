# Generated by Django 3.0.8 on 2020-08-04 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_remove_listing_currentbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='currentbid',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.CurrentBid'),
        ),
    ]