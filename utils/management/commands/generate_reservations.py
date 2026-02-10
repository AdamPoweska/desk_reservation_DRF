from django.core.management.base import BaseCommand
from desk_reservation.models import Floor, Desk, Reservation
from django.contrib.auth import get_user_model
from datetime import date
import random

User = get_user_model() # we need it for ACTUAL user model in this project

def date_generator():
    year = random.randint(2024, 2026)
    month = random.randint(1, 12)

    days_in_months = {
        1: random.randint(1, 31),
        2: random.randint(1, 28),
        3: random.randint(1, 31),
        4: random.randint(1, 30),
        5: random.randint(1, 31),
        6: random.randint(1, 30),
        7: random.randint(1, 31),
        8: random.randint(1, 31),
        9: random.randint(1, 30),
        10: random.randint(1, 31),
        11: random.randint(1, 30),
        12: random.randint(1, 31),
    }

    day = days_in_months.get(month)
    return date(year=year, month=month, day=day)

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = list(User.objects.all())
        desks = list(Desk.objects.all())

        reservation_list = []
        
        for _ in range(100):
            desk = random.choice(desks)
            reservation_date = date_generator()
            one_user = random.choice(users)

            reservation_list.append(
                Reservation(
                    desk=desk,
                    reservation_date=reservation_date,
                    reservation_by=one_user
                )
            )

            print(desk, reservation_date, one_user)

        Reservation.objects.bulk_create(reservation_list)

        self.stdout.write(self.style.SUCCESS("Reservations generated"))