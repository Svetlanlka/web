# Generated by Django 3.2 on 2021-04-19 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_dislike',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='answer',
            name='is_like',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='is_dislike',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='is_like',
            field=models.BooleanField(default=False),
        ),
    ]
