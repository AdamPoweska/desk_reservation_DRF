# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from desk_reservation.models import Floor, Desk, Reservation
from desk_reservation.serializers import *
from django.db.models import Q


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        elif request.user and request.user.is_superuser:
            return True


class FloorViewSet(viewsets.ModelViewSet):
    """
    CRUD actions.
    """
    # queryset = Floor.objects.filter(floor_number__endswith=0) | Floor.objects.filter(floor_number__startswith=2) # | == OR
    # queryset = Floor.objects.filter(~Q(floor_number=1) & ~Q(floor_number__startswith=2) & ~Q(floor_number__startswith=3)) # ~ == NOT, & == AND (in Q we use "&" as AND, the usuall comma "," will act simillary to & but it will not allow to group: "filter(Q(A) | Q(B), Q(C))" is not equal to "filter(Q(A) | (Q(B) & Q(C)))")
    queryset = Floor.objects.all().order_by('floor_number')
    # print(queryset)
    # print(queryset.query)
    serializer_class = FloorSerializer
    permission_classes = [IsReadOnly]


class DeskViewSet(viewsets.ModelViewSet):
    """
    CRUD actions.
    """
    serializer_class = DeskSerializer
    # https://stackoverflow.com/questions/49134679/drf-check-if-an-object-already-exist-in-db-when-receiving-a-request
    queryset = Desk.objects.all().order_by('floor', 'desk_number')
    # queryset = Desk.objects.filter(floor__floor_number=1)
    permission_classes = [IsReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        floor = serializer.validated_data.get('floor')
        desk_number = serializer.validated_data.get('desk_number')
        
        if desk_number is None or str(desk_number).strip() == "":
            return Response({'message': 'Desk can not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        """
        get_or_create - Returns a tuple of (object, created), where object is the retrieved or created object 
        and created is a boolean specifying whether a new object was created.
        If an object is found, get_or_create() returns a tuple of that object and False. created = False, defaults= is ignored
        If an object is not found, get_or_create() creates a new object. defaults= <- additional fields for creating object
        """
        desk, created = Desk.objects.get_or_create(
            floor=floor,
            desk_number=desk_number,
            defaults=serializer.validated_data
        )

        if created == False:
            return Response({'message': 'Desk number already exists on given floor'}, status=status.HTTP_400_BAD_REQUEST)
        

        """
        Zgodność z REST — po POST powinieneś zwrócić 201 Created i w nagłówku 
        Location podać adres nowo utworzonego zasobu.

        Klient API (np. frontend, Postman, inny mikroserwis) może dzięki temu od razu przejść do tego zasobu, 
        bez szukania jego id.
        
        Nagłówek wyświetli się tylko jeżeli mamy HyperlinkedModelSerializer albo dodamy nagłówek 'url' ręcznie.
        """
        headhers = self.get_success_headers(serializer.data)
        return Response(
            DeskSerializer(desk).data,
            status=status.HTTP_201_CREATED,
            headers=headhers
        )


class FloorDeskNestedViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    # queryset = Desk.objects.all()
    # queryset = Floor.objects.prefetch_related('desk_set') # lepsza optymalizacja niż linia wyżej ale linia wyżej też bedzie w 100% działać
    serializer_class = FloorDeskNestedSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return Floor.objects.filter(floor_num=self.kwargs['desk'])

        
class WorkerViewSet(viewsets.ModelViewSet):
    """
    CRUD actions.
    """
    queryset = User.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [permissions.IsAdminUser]


class ReservationViewSet(viewsets.ModelViewSet):
    """
    Making reservations - CRUD.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsReadOnly]
