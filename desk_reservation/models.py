from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Floor(models.Model):
    floor_number = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])


class Desk(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    desk_number = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)], unique=True)
    reservation = models.BooleanField()

    class Meta:
        def __repr__(self):
            return f"{self.floor}-{self.desk_number}"
        
'''
class Worker(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    id_number = models.IntegerField(validators=[MinValueValidator(1)], unique=True)

    def __repr__(self):
        return f"{self.name}{self.surname}-{self.id_number}"
'''