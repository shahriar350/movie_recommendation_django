# Generated by Django 4.1 on 2022-12-16 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('movies', models.ManyToManyField(related_name='get_director_movies', to='movie_app.movie')),
            ],
        ),
        migrations.DeleteModel(
            name='MovieDirector',
        ),
    ]