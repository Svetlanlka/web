# Generated by Django 3.2 on 2021-04-19 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20210419_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='photo_url',
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
    ]
