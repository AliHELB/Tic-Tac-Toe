# Generated by Django 5.0 on 2023-12-25 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morpion', '0014_game_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_player',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
