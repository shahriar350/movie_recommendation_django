# Generated by Django 4.1 on 2022-12-16 22:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie_app', '0002_director_delete_moviedirector'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='movierating',
            unique_together={('user', 'movie')},
        ),
    ]
