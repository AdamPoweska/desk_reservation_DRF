from django.contrib.auth.models import User, AbstractUser
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from desk_reservation.models import *


class FloorSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Floor model.
    """
    class Meta:
        model = Floor
        fields = ['id', 'floor_number']
        validators = [
            UniqueTogetherValidator(
                queryset=Floor.objects.all(),
                fields=['floor_number']
            )
        ]


class DeskSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Desk model.
    """
    class Meta:
        model = Desk
        fields = ['id', 'floor', 'desk_number']
    
    # def validate_desk_number(self, value):
    #     if not value:
    #         raise serializers.ValidationError("Desk can not be empty")
    #     return value


class SmallDeskSerializer(serializers.ModelSerializer):
    """
    Smaller serializer for Desk model - excludes 'floor' field.
    """
    class Meta:
        model = Desk
        fields = ['id', 'desk_number']


class FloorDeskNestedSerializerOne(serializers.ModelSerializer):
    """
    Nested serializer Floor > Desk, which uses only 'id', 'desk_number' fields from Desk model.
    """
    desks_on_floor = SmallDeskSerializer(many=True, read_only=True)

    class Meta:
        model = Floor
        fields = ['id', 'floor_number', 'desks_on_floor'] # wpisując 'desk_set' odwołamy się do ukrytego pola w modelu Floor - ale zwróci on tylko pk a nie wartości obiektów
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Desk.objects.all(),
        #         fields=['floor_number', 'desk_number']
        #     )
        # ]
    
    # def validate_desk_number(self, value):
    #     if not value:
    #         raise serializers.ValidationError("Desk can not be empty")
    #     return value

class FloorDeskNestedSerializerTwo(serializers.ModelSerializer):
    """
    Nested serializer Floor > Desk, which uses all fields from Desk model.
    """
    desks_on_floor = DeskSerializer(many=True, read_only=True)

    class Meta:
        model = Floor
        fields = ['id', 'floor_number', 'desks_on_floor']


class FloorDeskNestedSerializerThree(serializers.ModelSerializer):
    """
    Nested serializer Floor > Desk, which shows PK values from Desk model.
    """
    desks = serializers.PrimaryKeyRelatedField(queryset=Floor.objects.all(), source='desks_on_floor', many=True)

    class Meta:
        model = Floor
        fields = ['id', 'floor_number', 'desks']


class FloorDeskNestedSerializerFour(serializers.ModelSerializer):
    """
    Nested serializer Floor > Desk, which uses 'get_' functions to obtain data from Desk model.
    """
    desk = serializers.SerializerMethodField()

    class Meta:
        model = Floor
        fields = ['id', 'floor_number', 'desk']

    def get_desk(self, obj):
        # Filter only desks numbers: https://www.geeksforgeeks.org/python/how-to-filter-a-nested-serializer-in-django-rest-framework/
        return [
            {
                'desk': c.desk_number
            }
            for c in obj.desks_on_floor.all()
        ]


class FloorDeskNestedSerializerFive(serializers.ModelSerializer):
    """
    Nested serializer Floor > Desk, which shows __str__ values from Desk model.
    """
    desks_on_floor = serializers.StringRelatedField(many=True)

    class Meta:
        model = Floor
        fields = ['id', 'floor_number', 'desks_on_floor']


class FloorDeskNestedSerializerSix(serializers.ModelSerializer):
    """
    Nested serializer Floor > Desk, which shows PK values from Desk model using SlugRelatedField.
    """
    desks_on_floor = serializers.SlugRelatedField(many=True, read_only=True, slug_field='desk_number')

    class Meta:
        model = Floor
        fields = ['id', 'floor_number', 'desks_on_floor']


class WorkerSerializer(serializers.ModelSerializer):
    """
    Serializer for User from django.contrib.auth.models.
    """
    # desk_reservation = serializers.PrimaryKeyRelatedField(many=True, queryset=Desk.objects.all())
    # password_check = serializers.BooleanField(label="Generate password automatically?", required=False, default=True) # write_only=True sprawi że hasło będzie można tylko zapisać ale już nie odczytać
    password = serializers.CharField(required=False, help_text='password will be generated automatically', write_only=False) # write_only=True - chroni hasło, żeby nie wysyłać go w odpowiedzi API

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
    
    def create(self, validated_data):
        validated_data.pop('password', None) # .pop on variable itself will remove it fully from dictionary, if we would use "validated_data.pop('password', None)" - we could still use password given by the admin
        password = User.objects.make_random_password()
        user = User.objects.create_user(password=password, **validated_data)
        
        user._generated_password = password # w pythonie możemy dodać atrybut dynamicznie do obiektu (składnia pythona a nie django/drf). "_generated_password" nie zostanie nigdzie zapisane - bo nie ma takiego pola w serializerze. Jednak będzie działać jeszcze z return i dlatego będzie można je zobaczyć jeden raz - i tylko ten jeden raz.
        return user
    
    def to_representation(self, instance): # "To implement a custom relational field, you should override RelatedField, and implement the .to_representation(self, value) method."
        data = super().to_representation(instance) # super() tworzy klasę która dziedziczy wszystkie metody i właściwości innej klasy -> w tym przypadku super() jest wywoływane na funkcji a nie klasie. W takim wypadku super() wywołuje METODĘ O TEJ NAZWIE Z KLASY NADRZĘDNEJ
        if hasattr(instance, '_generated_password'): # jeżeli instance ma _generated_password
            data['generated_password'] = instance._generated_password # to dodajemy klucz "generated_password" do słownika DATA i nadajemy mu wartość która była przekazana do funkcji jako INSTANCE
        return data


class SmallReservationSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Reservation model with no additional options.
    """
    class Meta:
        model = Reservation
        fields = ['desk', 'reservation_date', 'reservation_by']


class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for Reservation model, UniqueTogetherValidator applied, "desk_ids" field is write_only, "reservation_by" is read_only.
    "desk_ids" show __str__ of Desk model.
    """
    #https://stackoverflow.com/questions/26561640/django-rest-framework-read-nested-data-write-integer
    #https://dev.to/forhadakhan/automatically-add-logged-in-user-under-createdby-and-updatedby-to-model-in-django-rest-framework-4c9c
    desk = DeskSerializer(read_only=True)
    desk_ids = serializers.PrimaryKeyRelatedField(write_only=True, source='desk', queryset=Desk.objects.all())
    reservation_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'desk_ids', 'desk', 'reservation_date', 'reservation_by']
        validators = [
            UniqueTogetherValidator(
                queryset=Reservation.objects.all(),
                fields=['desk_ids', 'reservation_date']
            ),
            UniqueTogetherValidator(
                queryset=Reservation.objects.all(),
                fields=['reservation_date', 'reservation_by']
            )
        ]


class FullReservationSerializer(serializers.ModelSerializer):
    """
    Full serializer for Reservation model, UniqueTogetherValidator applied, "desk_ids" field is write_only, "reservation_by" is read_only.
    Floor and Desk number can be posted in separate fields.
    """   
    # writable ForeignKey for create()
    # desk = serializers.PrimaryKeyRelatedField(read_only=True)
    # floor = serializers.PrimaryKeyRelatedField(read_only=True)
    
    # fields for writing only
    floor_number = serializers.IntegerField(write_only=True)
    desk_number = serializers.IntegerField(write_only=True)
    
    reservation_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), 
        read_only=True
    )

    # fields to show not as PK but as actual values
    desk_display = serializers.SerializerMethodField()
    floor_display = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            # 'id',
            # 'floor',
            'floor_number',
            'floor_display',
            # 'desk',
            'desk_number',
            'desk_display',
            'reservation_date',
            'reservation_by'
        ]
        
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Reservation.objects.all(),
        #         fields=['desk', 'reservation_date']
        #     ),
            # UniqueTogetherValidator(
            #     queryset=Reservation.objects.all(),
            #     fields=['reservation_date', 'reservation_by']
            # )
        # ]
    
    # def get_desk(self, obj):
    #     return obj.desk.desk_number

    def get_desk_display(self, obj):
        return obj.desk.desk_number
    
    # def get_floor(self, obj):
    #     return obj.desk.floor.floor_number
    
    def get_floor_display(self, obj):
        return obj.desk.floor.floor_number
    
    # def validate(self, data):
    #     floor_number = data.get('floor_number')
    #     desk_number = data.get('desk_number')
        
    #     floor, _ = Floor.objects.get_or_create(floor_number=floor_number)
    #     desk, _ = Desk.objects.get_or_create(desk_number=desk_number, floor=)

    #     data['floor'] = floor
    #     data['desk'] = desk

    #     return data
    
    # create is not needed - overriding it with above validate
    def create(self, validated_data):
        desk_number = validated_data.pop('desk_number')
        floor_number = validated_data.pop('floor_number')

        # desk = Desk.objects.get(id=desk_id)
        floor = Floor.objects.get(floor_number=floor_number)
        # floor = Floor.objects.get(id=floor_id)
        desk = Desk.objects.get(desk_number=desk_number, floor=floor)

        # validated_data['desk'] = desk
        # validated_data['floor'] = floor

        reservation = Reservation.objects.create(
            desk=desk,
            # floor=floor,
            reservation_date=validated_data['reservation_date'],
            reservation_by=self.context['request'].user  # jeśli chcesz ustawiać user
        )

        return reservation
        

class SmallReservationSerializer(serializers.ModelSerializer):
    reservation_by = serializers.StringRelatedField(read_only=True) #StringRelatedField = if there is related object (ForeignKey), then show it as string

    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_by']


class NestedDeskReservationSerializer(serializers.ModelSerializer):
    reservations = SmallReservationSerializer(many=True, read_only=True)
 
    class Meta:
        model = Desk
        fields = ['desk_number', 'reservations']


class FullReservationDataForHumansSerializer(serializers.ModelSerializer):
    desks_on_floor = NestedDeskReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Floor
        fields = ['floor_number', 'desks_on_floor']


class NestedDeskReservationForMachinesSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(many=True, read_only=True)
 
    class Meta:
        model = Desk
        fields = ['desk_number', 'reservations']


class FullReservationDataForMachinesSerializer(serializers.ModelSerializer):
    desks_on_floor = NestedDeskReservationForMachinesSerializer(many=True, read_only=True)

    class Meta:
        model = Floor
        fields = ['floor_number', 'desks_on_floor']


class MinimalDeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ['desk_number']


class MinimalFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['floor_number']


class FullReservationDataForFilterSerializer(serializers.ModelSerializer):
    floor_number = serializers.IntegerField(source='desk.floor.floor_number')
    desk_number = serializers.IntegerField(source='desk.desk_number')
    reservation_by = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = ['floor_number', 'desk_number', 'reservation_date', 'reservation_by']


class FullReservationSerializerForExactFilter(serializers.ModelSerializer):
    reservation_by = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_by']


class FilterSerializerWithEpmtyDesks(serializers.ModelSerializer):
    reservations = FullReservationSerializerForExactFilter(many=True)

    class Meta:
        model = Desk
        fields = ['floor', 'desk_number', 'reservations']
  
    
class DeskAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ["floor", "desk_number"]
