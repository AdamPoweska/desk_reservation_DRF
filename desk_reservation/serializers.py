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
    
    def validate_desk_number(self, value):
        if not value:
            raise serializers.ValidationError("Desk can not be empty")
        return value


class WorkerSerializer(serializers.ModelSerializer):
    # desk_reservation = serializers.PrimaryKeyRelatedField(many=True, queryset=Desk.objects.all())
    # password_check = serializers.BooleanField(label="Generate password automatically?", required=False, default=True) # write_only=True sprawi że hasło będzie można tylko zapisać ale już nie odczytać
    password = serializers.CharField(required=False, help_text='password will be generated automatically', write_only=False) # write_only=True - chroni hasło, żeby nie wysyłać go w odpowiedzi API

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        password = User.objects.make_random_password()
        user = User.objects.create_user(password=password, **validated_data)
        
        return user

"""
def create(self, validated_data):
    return User.objects.create_user(**validated_data)
"""

"""
def create(self, validated_data):
    password = validated_data.pop('password', None)
    if not password:
        password = User.objects.make_random_password()
    user = User.objects.create_user(password=password, **validated_data)
    return user
"""


'''
class UserSerializer(serializers.ModelSerializer):
    # desk_reservation = serializers.PrimaryKeyRelatedField(many=True, queryset=Desk.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username']
'''