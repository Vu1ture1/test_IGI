# Generated by Django 4.2.13 on 2024-05-19 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_promocode_myuser_my_promocodes'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='discount',
            field=models.FloatField(default=5),
        ),
    ]
