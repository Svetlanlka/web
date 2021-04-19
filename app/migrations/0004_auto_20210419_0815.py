# Generated by Django 3.2 on 2021-04-19 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210419_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='None', max_length=255),
        ),
    ]