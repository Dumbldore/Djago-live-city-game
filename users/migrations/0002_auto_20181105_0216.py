# Generated by Django 2.1.3 on 2018-11-05 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='people',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]