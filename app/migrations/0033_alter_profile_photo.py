# Generated by Django 3.2 on 2021-06-17 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='cat-smart.jpg', upload_to=''),
        ),
    ]
