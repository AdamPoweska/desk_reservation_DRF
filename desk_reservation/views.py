# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from desk_reservation.models import Floor, Desk
from desk_reservation.serializers import FloorSerializer, DeskSerializer, WorkerSerializer


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.is_superuser:
            return True


class FloorViewSet(viewsets.ModelViewSet):
    """
    CRUD actions.
    """
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsReadOnly]
    # permission_classes = [permissions.IsAdminUser]


class DeskViewSet(viewsets.ModelViewSet):
    """
    CRUD actions.
    """
    # https://stackoverflow.com/questions/49134679/drf-check-if-an-object-already-exist-in-db-when-receiving-a-request
    queryset = Desk.objects.all()
    serializer_class = DeskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
        
        
class WorkerViewSet(viewsets.ModelViewSet):
    """
    CRUD actions.
    """
    queryset = User.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]