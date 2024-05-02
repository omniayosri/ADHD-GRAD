from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class PatientProfile(models.Model):
    user = models.OneToOneField(User,
                                related_name='patient',
                                on_delete=models.CASCADE
                                )
    

    def __str__(self) -> str:
        return f'Patient {self.user}'
    


class TaskQuerySet(models.QuerySet):
    def is_trash(self):
        return self.filter(trash=False)
    
    def is_hidden(self):
        return self.filter(hidden=False)
    
    def is_active(self):
        return self.filter(active=True)
    
    def search(self, query, patient):
        lookups = Q(title__icontains=query) | Q(purpose__icontains=query)
        qs = self.is_active().is_hidden().is_trash().filter(patient=patient).filter(lookups)
        return qs
    


class TaskManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return TaskQuerySet(self.model, using=self._db)
    
    def get_tasks(self):
        return self.get_queryset().is_active().is_trash().is_hidden()
    
    def create(self, **kwargs: Any) -> Any:
        return super().create(**kwargs)
    
    def custom_all(self, patient):
        return self.all().filter(patient=patient)
    
    def get_trash(self, patient):
        return self.get_queryset().filter(patient=patient).filter(trash=True)
    
    def get_favorites(self, patient):
        return self.get_queryset().filter(patient=patient).filter(favorite=True)
    
    def get_hidden(self, patient):
        return self.get_queryset().filter(patient=patient).filter(hidden=True)
    
    def search(self,query, patient):
        return self.get_queryset().search(query, patient)
    


class Task(models.Model):
    patient = models.ForeignKey(PatientProfile,
                                related_name='patient_tasks',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    purpose = models.CharField(max_length=250)
    start_time = models.TimeField()
    end_time = models.TimeField()

    PRIORITY_CHOICES = [
        ('LW', 'Low'),
        ('MD', 'Medium'),
        ('HG', 'High')
    ]
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES)
    description = models.TextField()
    reminder = models.BooleanField(default=False)
    trash = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = TaskManager()

    def __str__(self) -> str:
        return f'Task {self.title} for {self.patient}'

