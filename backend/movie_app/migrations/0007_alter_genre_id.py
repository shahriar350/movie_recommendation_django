# Generated by Django 4.1 on 2022-12-23 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0006_movie_poster_alter_movie_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
