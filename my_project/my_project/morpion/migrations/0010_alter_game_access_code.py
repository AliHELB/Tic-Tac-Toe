# Generated by Django 5.0 on 2023-12-19 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morpion', '0009_game_access_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='access_code',
            field=models.CharField(blank=True, max_length=8, unique=True),
        ),
    ]
