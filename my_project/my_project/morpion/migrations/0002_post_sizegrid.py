# Generated by Django 4.2.7 on 2023-12-05 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morpion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='sizegrid',
            field=models.IntegerField(default=3),
        ),
    ]
