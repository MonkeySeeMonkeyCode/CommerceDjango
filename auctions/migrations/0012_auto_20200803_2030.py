# Generated by Django 3.0.8 on 2020-08-04 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20200803_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biditem', to='auctions.Listing'),
        ),
    ]
