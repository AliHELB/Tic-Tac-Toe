# Generated by Django 4.2.7 on 2023-12-05 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morpion', '0002_post_sizegrid'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='grid',
            field=models.CharField(default='', max_length=255),
        ),
    ]
