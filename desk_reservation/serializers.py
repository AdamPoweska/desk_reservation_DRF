from django.contrib.auth.models import User
from rest_framework import serializers
from desk_reservation.models import Floor, Desk


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['floor_number']


class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ['floor', 'desk_number', 'reservation']


class UserSerializer(serializers.ModelSerializer):
    # desk_reservation = serializers.PrimaryKeyRelatedField(many=True, queryset=Desk.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username']