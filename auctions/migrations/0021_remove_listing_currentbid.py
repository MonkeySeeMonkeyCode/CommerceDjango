# Generated by Django 3.0.8 on 2020-08-04 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20200803_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='currentbid',
        ),
    ]
