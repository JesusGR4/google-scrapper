# Generated by Django 2.2.11 on 2020-03-12 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place_info', '0002_auto_20200312_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeinfo',
            name='place_id',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
