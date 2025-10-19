from django.contrib.auth.models import User, AbstractUser
from rest_framework import serializers
from desk_reservation.models import Floor, Desk


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['id', 'floor_number']


class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ['id', 'floor', 'desk_number', 'reservation']


class WorkerSerializer(serializers.ModelSerializer):
    # desk_reservation = serializers.PrimaryKeyRelatedField(many=True, queryset=Desk.objects.all())

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


'''
class UserSerializer(serializers.ModelSerializer):
    # desk_reservation = serializers.PrimaryKeyRelatedField(many=True, queryset=Desk.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username']
'''