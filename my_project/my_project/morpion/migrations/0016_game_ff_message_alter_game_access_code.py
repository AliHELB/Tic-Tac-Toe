# Generated by Django 5.0 on 2024-01-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morpion', '0015_alter_game_current_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='ff_message',
            field=models.CharField(default='a', max_length=255),
        ),
        migrations.AlterField(
            model_name='game',
            name='access_code',
            field=models.CharField(blank=True, default='a', max_length=8, unique=True),
        ),
    ]
