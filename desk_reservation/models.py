from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Floor(models.Model):
    floor_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], unique=True)

    def __str__(self):
        return f"{self.floor_number}"

    def __repr__(self):
        return f"{self.floor_number}"


class Desk(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    desk_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], blank=False, null=False)

    def __str__(self):
        return f"Floor: {self.floor} Desk: {self.desk_number}"

    def __repr__(self):
        return f"{self.floor}-{self.desk_number}"


class Reservation(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    reservation_date = models.DateField()
