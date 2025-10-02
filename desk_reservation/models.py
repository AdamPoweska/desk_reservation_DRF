from django.db import models


class Floor(models.Model):
    floor_number = models.IntegerField(max_value=10, min_value=1)

class Desk(models.Model):
    desk_number = models.IntegerField(max_value=100, min_value=1)
    floor = models.ForeignKey(Floor)
    reservation = models.BooleanField()

    class Meta:
        def __repr__(self):
            return f"{self.floor}-{self.desk_number}"