# Generated by Django 5.0 on 2023-12-19 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morpion', '0007_game_gameover'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]