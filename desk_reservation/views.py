from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from desk_reservation.models import *
from desk_reservation.serializers import *
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
import django_filters

class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        elif request.user and request.user.is_superuser:
            return True


class FloorViewSet(viewsets.ModelViewSet):
    """
    CRUD actions - Floors.
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
    CRUD actions - Desks on related Floors.
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

        
        # get_or_create - Returns a tuple of (object, created), where object is the retrieved or created object 
        # and created is a boolean specifying whether a new object was created.
        # If an object is found, get_or_create() returns a tuple of that object and False. created = False, defaults= is ignored
        # If an object is not found, get_or_create() creates a new object. defaults= <- additional fields for creating object
        
        desk, created = Desk.objects.get_or_create(
            floor=floor,
            desk_number=desk_number,
            defaults=serializer.validated_data
        )

        if created == False:
            return Response({'message': 'Desk number already exists on given floor'}, status=status.HTTP_400_BAD_REQUEST)
        

        # Zgodność z REST — po POST powinieneś zwrócić 201 Created i w nagłówku 
        # Location podać adres nowo utworzonego zasobu.

        # Klient API (np. frontend, Postman, inny mikroserwis) może dzięki temu od razu przejść do tego zasobu, 
        # bez szukania jego id.
        
        # Nagłówek wyświetli się tylko jeżeli mamy HyperlinkedModelSerializer albo dodamy nagłówek 'url' ręcznie.

        headhers = self.get_success_headers(serializer.data)
        return Response(
            DeskSerializer(desk).data,
            status=status.HTTP_201_CREATED,
            headers=headhers
        )


class FloorDeskNestedViewSetOne(viewsets.ModelViewSet):
    """
    This View set uses smaller serializer with only needed fields from Desk model: 'id', 'desk_number'. Fields can be easily changed in SmallDeskSerializer.
    """
    queryset = Floor.objects.all()
    # queryset = Desk.objects.all()
    # queryset = Floor.objects.prefetch_related('desk_set') # lepsza optymalizacja niż linia wyżej ale linia wyżej też bedzie w 100% działać
    serializer_class = FloorDeskNestedSerializerOne
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return Floor.objects.filter(floor_num=self.kwargs['desk'])

class FloorDeskNestedViewSetTwo(viewsets.ModelViewSet):
    """
    This is usual nested serializer on reversed relation using full model data from related model.
    """
    queryset = Floor.objects.all()
    # queryset = Desk.objects.all()
    # queryset = Floor.objects.prefetch_related('desk_set') # lepsza optymalizacja niż linia wyżej ale linia wyżej też bedzie w 100% działać
    serializer_class = FloorDeskNestedSerializerTwo
    permission_classes = [permissions.IsAuthenticated]


class FloorDeskNestedViewSetThree(viewsets.ModelViewSet):
    """
    This nested serializer uses 'PrimaryKeyRelatedField' on reversed relation. Only PK are shown.
    """
    queryset = Floor.objects.all()
    # queryset = Desk.objects.all()
    # queryset = Floor.objects.prefetch_related('desk_set') # lepsza optymalizacja niż linia wyżej ale linia wyżej też bedzie w 100% działać
    serializer_class = FloorDeskNestedSerializerThree
    permission_classes = [permissions.IsAuthenticated]


class FloorDeskNestedViewSetFour(viewsets.ModelViewSet):
    """
    This nested serializer is done by using 'SerializerMethodField'. We override 'get_' function to pass only desks numbers into variable.
    """
    queryset = Floor.objects.all()
    # queryset = Desk.objects.all()
    # queryset = Floor.objects.prefetch_related('desk_set') # lepsza optymalizacja niż linia wyżej ale linia wyżej też bedzie w 100% działać
    serializer_class = FloorDeskNestedSerializerFour
    permission_classes = [permissions.IsAuthenticated]


class FloorDeskNestedViewSetFive(viewsets.ModelViewSet):
    """
    This nested serializer is done by using 'StringRelatedField'.
    """
    queryset = Floor.objects.all()
    # queryset = Desk.objects.all()
    # queryset = Floor.objects.prefetch_related('desk_set') # lepsza optymalizacja niż linia wyżej ale linia wyżej też bedzie w 100% działać
    serializer_class = FloorDeskNestedSerializerFive
    permission_classes = [permissions.IsAuthenticated]


class FloorDeskNestedViewSetSix(viewsets.ModelViewSet):
    """
    This nested serializer is done by using 'SlugRelatedField'.
    """
    queryset = Floor.objects.all()
    # queryset = Desk.objects.all()
    # queryset = Floor.objects.prefetch_related('desk_set') # lepsza optymalizacja niż linia wyżej ale linia wyżej też bedzie w 100% działać
    serializer_class = FloorDeskNestedSerializerSix
    permission_classes = [permissions.IsAuthenticated]

        
class WorkerViewSet(viewsets.ModelViewSet):
    """
    CRUD actions - Workers.
    """
    queryset = User.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [permissions.IsAdminUser]


class ReservationViewSet(viewsets.ModelViewSet):
    """
    Making reservations - CRUD. We use 'desk_ids' nested serializer which is write_only and 'desk' nested serializer which is read_only.
    Validators will only allow for one user to make one desk reservation for one date.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(reservation_by=self.request.user)
    

class FullReservationViewSet(viewsets.ModelViewSet):
    """
    Making reservations - CRUD. We use separate "desk_number" and "floor_number" fields for POST.
    Validators will only allow for one user to make one desk reservation for one date.
    """
    queryset = Reservation.objects.all()
    serializer_class = FullReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(reservation_by=self.request.user)


class FullReservationDataForHumansViewSet(viewsets.ModelViewSet):
    """
    Reservation data - JSON trimmed for human eye.
    """
    queryset = Floor.objects.all()
    serializer_class = FullReservationDataForHumansSerializer
    permission_classes = [permissions.IsAdminUser]


class FullReservationDataForMachinesViewSet(viewsets.ModelViewSet):
    """
    Reservation data - FULL JSON for machines.
    """
    queryset = Floor.objects.all()
    serializer_class = FullReservationDataForMachinesSerializer
    permission_classes = [permissions.IsAdminUser]


class FilterDataViewSet(generics.ListAPIView):
    # https://django-filter.readthedocs.io/en/stable/
    """
    Basic view with django_filters. 
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'desk': ['exact'],
        'reservation_date': ['exact'],
        'reservation_by': ['exact'],
    }


class FloorFilter(FilterSet):
    """
    Filter for FloorFilterViewSet.
    """
    floor_number = django_filters.NumberFilter(
        field_name='floor'
    )

    class Meta:
        model = Desk
        fields = ['floor_number']

class FloorFilterViewSet(generics.ListAPIView):
    """
    1st level filter allowing for filtering by floor number, showing floor and related desks.
    """
    queryset = Desk.objects.all()
    serializer_class = DeskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FloorFilter


class ExactFilter(FilterSet):
    """
    Filter for ExactFilterViewSet.
    """
    floor_number = django_filters.NumberFilter(
        field_name='floor'
    )
    desk_number = django_filters.NumberFilter(
        field_name='desk_number'
    )

    class Meta:
        model = Desk
        fields = ['floor_number', 'desk_number']


# class ExactFilterViewSet(generics.ListAPIView):
#     queryset = Desk.objects.all()
#     serializer_class = DeskSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = ExactFilter


class FinalExactFilter(FilterSet):
    """
    Filter for FullReservationDataForFilterView.
    """
    floor_number = django_filters.NumberFilter(
        field_name='desk__floor__floor_number'
    )
    desk_number = django_filters.Filter(
        field_name='desk__desk_number'
    )

    class Meta:
        model = Reservation
        fields = ['floor_number', 'desk_number', 'reservation_date', 'reservation_by'] #'floor_number',


class FullReservationDataForFilterView(generics.ListAPIView):
    """
    View to show data in concise way:
    {
        "floor_number": ...,
        "desk_number": ...,
        "reservation_date": ...,
        "reservation_by": ...
    },
    """
    queryset = Reservation.objects.all()
    serializer_class = FullReservationDataForFilterSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FinalExactFilter


# class SmallReservationViewSet(viewsets.ModelViewSet):
#     queryset = Reservation.objects.all()
#     serializer_class = FullReservationDataForFilterSerializer
#     permission_classes = [permissions.IsAdminUser]


class FinalExactFilterWithEmptyDesks(FilterSet):
    """
    Filter for FullReservationDataForFilterWithEmptyDesksView .
    """
    reservation_date = django_filters.DateFilter(
        field_name='reservations__reservation_date'
    )
    reservation_by = django_filters.Filter(
        field_name='reservations__reservation_by'
    )

    class Meta:
        model = Desk
        fields = ['floor', 'desk_number', 'reservation_date', 'reservation_by']


class FullReservationDataForFilterWithEmptyDesksView(generics.ListAPIView):
    """
    View which will show also desk with no reservations.
    """
    queryset = Desk.objects.all().distinct() # distinct usuwa powielenia
    serializer_class = FilterSerializerWithEpmtyDesks
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FinalExactFilterWithEmptyDesks


class DeskAvailabilityFilter(FilterSet):
    """
    Filter for DeskAvailabilityView.
    """
    date = django_filters.DateFilter(
        method="filter_by_date",
        label="Availability date"
    )

    class Meta:
        model = Desk
        fields = ["floor", "desk_number", "date"]

    def filter_by_date(self, queryset, name, value):
        return queryset.exclude(
            reservations__reservation_date=value,
            reservations__reservation_by__isnull=False
        )
    
class DeskAvailabilityView(generics.ListAPIView):
    """
    Returns list of available desks for given date.
    Date needs to be provided in order to receive list of empty desks.
    Floor and Desk number filters can be left blank.
    Only EPTY desks will be shown for given date.
    """
    queryset = Desk.objects.all()
    serializer_class = DeskAvailabilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeskAvailabilityFilter


