# Generated by Django 3.0.8 on 2020-08-04 00:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20200803_2042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='bid',
            new_name='current_bid',
        ),
        migrations.AlterField(
            model_name='bids',
            name='item',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='biditem', to='auctions.Listing'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ManyToManyField(related_name='listing_category', to='auctions.Category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='createdby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='init_bid',
            field=models.IntegerField(default=0),
        ),
    ]
