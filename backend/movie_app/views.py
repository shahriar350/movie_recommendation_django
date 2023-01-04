from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import pandas as pd
from movie_app.models import MovieRating, Movie, Genre
from movie_app.serializers import MovieCreateRatingSerializer, MovieRatingSerializer, MovieSerializer, GenreSerializer
from django.db.models import Case, When, Q


# Create your views here.
class MovieListCreateView(ModelViewSet):
    serializer_class = MovieSerializer
    # queryset = Movie.objects.all()
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = Movie.objects
        if 'name' in self.request.query_params or 'genre' in self.request.query_params:
            if 'genre' in self.request.query_params:
                genre = self.request.query_params['genre']

                if genre != 'null' and len(genre) > 0:
                    queryset = queryset.filter(genre__id=int(genre))
            if 'name' in self.request.query_params:
                print('name')
                name = self.request.query_params['name']
                if len(name) > 0:
                    print(queryset)
                    queryset = queryset.filter(name__icontains=name)

        return queryset.all()

    # def filter_queryset(self, queryset):
    #     if 'name' in self.request.query_params or 'genre' in self.request.query_params:
    #         if 'genre' in self.request.query_params:
    #             genre = self.request.query_params['genre']
    #
    #             if genre != 'null' and len(genre) > 0:
    #                 queryset = queryset.filter(get=int(genre))
    #         if 'name' in self.request.query_params:
    #             print('name')
    #             name = self.request.query_params['name']
    #             if len(name) > 0:
    #                 print(queryset)
    #                 queryset = queryset.filter(name__icontains=name)
    #
    #     return queryset.all()


class GenreListView(ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class MovieRatingView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MovieCreateRatingSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieRatingSerializer
        else:
            return self.serializer_class

    http_method_names = ['get', 'post', 'head']

    def get_queryset(self):
        return MovieRating.objects.filter(user=self.request.user).all()


# To get similar movies based on user rating
def get_similar(movie_name, rating, corrMatrix):
    print(corrMatrix)
    print(corrMatrix[movie_name])
    # print(f"rating {rating}, movie name: {movie_name}, corr: {corrMatrix}")
    similar_ratings = corrMatrix[movie_name] * (rating - 2)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings


class RecommendView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MovieSerializer

    def get_queryset(self):
        movie_df = pd.DataFrame(list(MovieRating.objects.all().values()))
        new_user = movie_df.user_id.unique().shape[0]
        current_user_id = self.request.user.id
        print("1")
        userRatings = movie_df.pivot_table(index=['user_id'], columns=[
            'movie_id'], values='rating')
        userRatings = userRatings.fillna(0, axis=1)
        corrMatrix = userRatings.corr(method='pearson')
        user = pd.DataFrame(list(MovieRating.objects.filter(user=self.request.user).values())).drop(['user_id', 'id'],
                                                                                                    axis=1)
        print("2")

        if len(user) > 0:
            user_filtered = [tuple(x) for x in user.values]
            movie_id_watched = [each[0] for each in user_filtered]
            similar_movies = pd.DataFrame()
            for movie, rating in user_filtered:
                similar_movies = similar_movies.append(get_similar(
                    movie, rating, corrMatrix), ignore_index=True)
            movies_id = list(similar_movies.sum(
            ).sort_values(ascending=False).index)

            movies_id_recommend = [
                each for each in movies_id if each not in movie_id_watched
                ]

            preserved = Case(*[When(pk=pk, then=pos)
                               for pos, pk in enumerate(movies_id_recommend)])
            movie_list = list(Movie.objects.filter(
                id__in=movies_id_recommend).order_by(preserved)[:10])
            return movie_list
        else:
            return Movie.objects.none()


class SingleMovieView(RetrieveAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()


class SingleMovieRatingByUserView(RetrieveAPIView, CreateAPIView):
    serializer_class = MovieRatingSerializer
    lookup_field = 'movie__id'

    def get_object(self):
        return MovieRating.objects.get(user=self.request.user, movie_id=self.kwargs.get('movie_id'))

    def create(self, request, *args, **kwargs):
        try:
            rating = self.get_object()
            rating.rating = request.data['rating']
            rating.save()
        except MovieRating.DoesNotExist:
            MovieRating.objects.create(
                user=self.request.user,
                movie_id=self.kwargs.get('movie_id'),
                rating=request.data['rating']
            )
        return Response(status=200)

    # def get_queryset(self):
    #     return MovieRating.objects.filter(user=self.request.user)
