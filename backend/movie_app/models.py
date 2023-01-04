from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import capfirst

User = get_user_model()


# Create your models here.
class Genre(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return capfirst(self.name)


class Movie(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, related_name="get_genre_movies")
    release_year = models.DateField()
    poster = models.CharField(null=True, blank=True, max_length=255)
    image = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name


#
# class Director(models.Model):
#     name = models.CharField(max_length=255)
#     movies = models.ManyToManyField(Movie, related_name="get_director_movies")
#
#     def __str__(self):
#         return self.name


class MovieRating(models.Model):
    class Meta:
        unique_together = ('user', 'movie')

    user = models.ForeignKey(User, related_name="get_user_ratings", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name="get_movie_ratings", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        return str(self.user.name) + " " + self.movie.name + " " + self.rating.__str__()
