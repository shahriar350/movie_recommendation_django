import datetime
import decimal
import io
import tempfile
import uuid
from math import floor
import faker
from PIL import Image
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import base64
from auth_app.models import Users
from faker import Faker
import random
import requests
from movie_app.models import Genre, Movie, MovieRating
from faker import Faker

fk = Faker()
import tmdbsimple as tmdb


class Command(BaseCommand):
    help = 'Creating dummy movie with real user'

    # def add_arguments(self, parser):
    #     parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        tmdb.API_KEY = '2d6088f0b7d5cce1173b1e0567d5d224'

        genres = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=2d6088f0b7d5cce1173b1e0567d5d224') \
            .json()['genres']
        with transaction.atomic():

            print(".", end="")
            Genre.objects.all().delete()
            Movie.objects.all().delete()
            MovieRating.objects.all().delete()
            for genre in genres:
                Genre.objects.create(
                    id=genre['id'],
                    name=genre['name'].lower()
                )
            for i in range(1, 30):
                movies = requests.get(
                    f'https://api.themoviedb.org/3/movie/popular?api_key=2d6088f0b7d5cce1173b1e0567d5d224&language=en-US&page={i}').json()[
                    'results']
                for movie in movies:
                    date = list(map(int, movie['release_date'].split("-")))

                    mov = Movie(
                        name=movie['title'],
                        description=movie['overview'],
                        release_year=datetime.date(year=date[0], month=date[1], day=date[2]),
                        image=f'https://image.tmdb.org/t/p/original/{movie["backdrop_path"]}',
                        poster=f'https://image.tmdb.org/t/p/original/{movie["poster_path"]}'
                    )
                    mov.save()

                    for gen in movie['genre_ids']:
                        mov.genre.add(gen)
