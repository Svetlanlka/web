# Generated by Django 3.2 on 2021-04-19 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210419_0807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='likes',
            new_name='rating',
        ),
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
