# Generated by Django 5.0 on 2023-12-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morpion', '0004_game_delete_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='alignement',
            field=models.IntegerField(default=3),
        ),
    ]