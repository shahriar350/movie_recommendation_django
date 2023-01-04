from django.contrib.auth import get_user_model
from rest_framework import serializers

from movie_app.models import MovieRating, Movie, Genre

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number']


class MovieRatingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie = MovieSerializer()

    class Meta:
        model = MovieRating
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'movie'),
                message="You already rated this movie once. You can update your rate or rate another movie."
            )
        ]


class MovieCreateRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MovieRating
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'movie'),
                message="You already rated this movie once. You can update your rate or rate another movie."
            )
        ]
