# Generated by Django 3.2 on 2021-04-19 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210419_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rating',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
