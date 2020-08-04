# Generated by Django 3.0.8 on 2020-08-03 23:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200803_1917'),
    ]

    operations = [
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
    ]