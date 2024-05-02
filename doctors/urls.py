from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.user_register_view, name='register'),
    path('retrieve/<str:email>/', views.UpdateDeleteRetrieveDoctorView.as_view(), name='retrieve'),
    path('delete/<str:email>/', views.UpdateDeleteRetrieveDoctorView.as_view(), name='delete'),
    path('update/<str:email>/', views.UpdateDeleteRetrieveDoctorView.as_view(), name='update'),
    path('list/', views.ListDoctorsView.as_view(), name='list'),
    
    path('create-time-slot/', views.CreateListFreeSlot.as_view(), name='create_slot'),
    path('list-time-slot/', views.CreateListFreeSlot.as_view(), name='list_slot'),
    path('create-appointment/', views.CreateListAppointment.as_view(), name='create_appointment'),
    path('list-appointment/', views.CreateListAppointment.as_view(), name='list_appointment'),
]