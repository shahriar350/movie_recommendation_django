from django.urls import path
from rest_framework import routers

from . import views

app_name = "movie"

router = routers.DefaultRouter()
router.register('rating/user', views.MovieRatingView, basename="rating")
router.register('list/create', views.MovieListCreateView, basename="list.create")

urlpatterns = [
    # path('list/create/', views.MovieListCreateView.as_view(), name='list.create'),
    path('genre/list/', views.GenreListView.as_view(), name='genre.list'),
    path('recommend/', views.RecommendView.as_view(), name='recommend'),
    path('rating/<int:movie_id>/', views.SingleMovieRatingByUserView.as_view(), name='single.movie.rating'),
    # path('rating/user/', views.MovieRatingView.as_view(), name='rating'),
]

urlpatterns = urlpatterns + router.urls
