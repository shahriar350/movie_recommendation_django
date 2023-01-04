from django.core.management.base import BaseCommand, CommandError
from auth_app.models import Users as User
from movie_app.models import Movie, MovieRating
from faker import Faker
fk = Faker()
import random
class Command(BaseCommand):
    
    def handle(self, *args, **options):
        # for i in range(9):
        #     user = User.objects.create_user(
        #         name=fk.name(),
        #         phone_number = "017524924{}7".format(i),
        #         password="123456"
        #     )
        users = User.objects.all()
        for user in users:
            for i in range(6):
                rand_movie_id = random.randint(3723,4303)
                mov = Movie.objects.get(pk=rand_movie_id)
                try:
                    MovieRating.objects.create(
                        movie = mov,
                        user = user,
                        rating = random.randint(4,9)
                    )
                except Exception as e:
                    print(e)
        
        
        
        