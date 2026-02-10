from django.core.management.base import BaseCommand
from desk_reservation.models import User
from faker import Faker


fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(1000):
            user_password = fake.password(length=10)

            user = User.objects.create_user(
                username=fake.unique.user_name(),
                first_name=fake.first_name(),
                last_name=fake.name(),
                email=fake.unique.email(),
                password=user_password,
            )
            print("login: ", user.username, "PW: ", user_password)

        self.stdout.write(self.style.SUCCESS("Users generated"))