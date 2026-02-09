from django.core.management.base import BaseCommand
from desk_reservation.models import Floor, Desk

class Command(BaseCommand):
    def handle(self, *args, **kwargs): # handle = unique, musi zostać: "The actual logic of the command. Subclasses must implement this method.
        for floor in Floor.objects.all():
            desks = [Desk(desk_number=i+1, floor=floor) for i in range(100)] # Python (lista) > ORM (QuerySet) > SQL (baza)
            Desk.objects.bulk_create(desks, ignore_conflicts=True) # we need to add "constraints =" in model for "ignore_conflicts=", it wont be working ontherwise
        
        self.stdout.write(self.style.SUCCESS("Desks generated")) # printing in shell
