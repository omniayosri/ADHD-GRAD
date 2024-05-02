from django.contrib import admin

from .models import DoctorProfile, FreeTimeSlot, Appointment

admin.site.register(DoctorProfile)
admin.site.register(FreeTimeSlot)
admin.site.register(Appointment)