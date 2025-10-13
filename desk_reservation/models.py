from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Floor(models.Model):
    floor_number = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])


class Desk(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    desk_number = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    reservation = models.BooleanField()

    class Meta:
        def __repr__(self):
            return f"{self.floor}-{self.desk_number}"
