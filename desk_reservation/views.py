# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from desk_reservation.models import Floor, Desk
from desk_reservation.serializers import FloorSerializer, DeskSerializer, WorkerSerializer


class FloorViewSet(viewsets.ModelViewSet):
    """
    CRUD actions.
    """
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DeskViewSet(viewsets.ModelViewSet):
    """
    CRUD actions.
    """
    queryset = Desk.objects.all()
    serializer_class = DeskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class WorkerViewSet(viewsets.ModelViewSet):
    """
    CRUD actions.
    """
    queryset = User.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]