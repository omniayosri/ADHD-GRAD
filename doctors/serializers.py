from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime

from .models import DoctorProfile, FreeTimeSlot, Appointment

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'Password Does not match'})
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})
        
        account = User(email = self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account
    



class DoctorRegistration(serializers.ModelSerializer):
    specialize = serializers.CharField()
    contact = serializers.IntegerField()
    address = serializers.CharField()
    experiance = serializers.IntegerField()
    birth_date = serializers.DateField()
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'specialize', 'contact', 'address', 'experiance', 'birth_date']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def save(self, **kwargs):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'Password Does not match'})
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})
        
        account = User(email = self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account
    


class DoctorRetrieveSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ['id','username', 'email', 'specialize', 'contact', 'address', 'experiance', 'birth_date', 'photo']




class DoctorFreeTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeTimeSlot
        fields = ['doctor', 'start_time', 'end_time']



class CreateAppointment(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'