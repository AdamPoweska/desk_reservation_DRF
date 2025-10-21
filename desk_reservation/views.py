# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
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
        
        # if not created:
        #     return Response(
        #         DeskSerializer(desk).data,
        #         status=status.HTTP_200_OK     
        #     )
        
        headhers = self.get_success_headers(serializer.data)
        return Response(
            DeskSerializer(desk).data,
            status=status.HTTP_201_CREATED,
            headers=headhers
        )

        # if created:
        #     return Response(DeskSerializer(desk).data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(DeskSerializer(desk).data, status=status.HTTP_200_OK)



        #     if desk_number != '':
        #         desk_list = Desk.objects.filter(floor=floor, desk_number=desk_number)

        #         if not desk_list:
        #             serializer.save()
        #         else:
        #             serializer = DeskSerializer(desk_list[0])
        #         return Response(serializer.data)
        #     else:
        #         return Response(data={'message': 'Empty desk_number'}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerViewSet(viewsets.ModelViewSet):
    """
    CRUD actions.
    """
    queryset = User.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]