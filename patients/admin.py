from django.contrib import admin

from .models import PatientProfile, Task

admin.site.register(PatientProfile)
admin.site.register(Task)