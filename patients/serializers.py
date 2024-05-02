from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Task, PatientProfile


class TaskSerializer(serializers.ModelSerializer):

    patient = serializers.CharField(source='patient.user.username')

    class Meta:
        model = Task
        fields = [
            'id',
            'patient',
            'title',
            'purpose',
            'start_time',
            'end_time',
            'priority',
            'description',
            'reminder'
        ]

    
    def create(self, validated_data):
        user = validated_data['patient']['user']['username']
        request = self.context.get('request')
        patient = get_object_or_404(PatientProfile, user=request.user.id)
        if request.user.username == user and patient is not None:
            validated_data['patient'] = patient
            return super().create(validated_data)
        else:
            raise serializers.ValidationError({'Message': 'You have validation error.'})
        
    
    def update(self, instance, validated_data):
        user = validated_data['patient']['user']['username']
        request = self.context.get('request')
        patient = get_object_or_404(PatientProfile, user=request.user.id)
        if request.user.username == user and patient is not None:
            validated_data['patient'] = patient
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError({'Message': 'You have validation error.'})
        
    



class PatientProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            'id',
            'username',
            'email'
        ]