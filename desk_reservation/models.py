from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Floor(models.Model):
    floor_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)]) # unique=True

    def __str__(self):
        return f"{self.floor_number}"

    def __repr__(self):
        return f"{self.floor_number}"


class Desk(models.Model):
    floor = models.ForeignKey(Floor, related_name='desks_on_floor', on_delete=models.CASCADE)
    desk_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], blank=False, null=False)

    def __str__(self):
        return f"Floor: {self.floor} > Desk: {self.desk_number}"

    def __repr__(self):
        return f"{self.floor}-{self.desk_number}"


class AvailableDates(models.Model):
    # https://forum.djangoproject.com/t/create-a-date-difference-generatedfield-in-model/38390/11
    # https://www.geeksforgeeks.org/python/creating-a-list-of-range-of-dates-in-python/?utm_source=chatgpt.com
    '''
    (1) DateRange - model z datami od do
    (2) Date - model już z samymi datami, który to faktycznie podczepiamy pof model DESK
        - trzeba bedzie zaimportować to do widoku
        - tam wygenerować listę za pomocą pand
        - zwrócić tą listę do modelu Date
    '''
    
    date_start = models.DateField()
    date_end = models.DateField()
    date = models.DateField()

class Reservation(models.Model):
    # floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    reservation_date = models.DateField()
