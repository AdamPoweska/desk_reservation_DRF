# from django.shortcuts import render
from rest_framework import permissions, viewsets
from desk_reservation.models import Floor, Desk
from desk_reservation.serializers import FloorSerializer, DeskSerializer


class FloorViewSet(viewsets.ModelViewSet):
    """
    `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DeskViewSet(viewsets.ModelViewSet):
    """
    `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Desk.objects.all()
    serializer_class = DeskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
