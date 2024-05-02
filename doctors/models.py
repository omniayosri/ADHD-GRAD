from django.db import models
from django.contrib.auth.models import User

def upload_photo(obj, photo_name):
    return f'Doctor_profile_pictures/{obj.user.username}/{photo_name}'



class DoctorProfile(models.Model):
    user = models.OneToOneField(User,
                                related_name='doctor',
                                on_delete=models.CASCADE
                                )
    
    specialize = models.CharField(max_length=100)
    contact = models.IntegerField()
    address = models.CharField(max_length=250)
    experiance = models.IntegerField()
    birth_date = models.DateField()
    photo = models.ImageField(upload_to=upload_photo, default='user.png')


    def __str__(self) -> str:
        return f'Doctor {self.user}'
    





class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorProfile, related_name='appointment', on_delete=models.CASCADE)
    patient = models.ForeignKey('patients.PatientProfile', related_name='appointment', on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.doctor.user.username} with {self.patient.user.username} on {self.date_time}"


class FreeTimeSlot(models.Model):
    doctor = models.ForeignKey(DoctorProfile, related_name='free_time', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.doctor.user.username} free from {self.start_time} to {self.end_time}'
    
