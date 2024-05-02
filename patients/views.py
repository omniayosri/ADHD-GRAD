from rest_framework.response import Response
from rest_framework.decorators import api_view
from oauth2_provider.models import AccessToken, RefreshToken
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404

from doctors.serializers import UserSerializer
from .models import PatientProfile, Task
from .serializers import TaskSerializer, PatientProfileSerializer
from doctors.models import Appointment
from doctors.serializers import CreateAppointment

@api_view(["POST"])
def user_register_view(request):
    serializer = UserSerializer(data=request.data)

    data = {}

    if serializer.is_valid():
        user = serializer.save()
        PatientProfile.objects.create(user=user)

        data["response"] = "Account for Patient has been created"
        data["username"] = user.username
        data["email"] = user.email

        token = AccessToken.objects.get(user=user)
        refresh_token = RefreshToken.objects.get(user=user)
        data["token"] = token.token
        data["refresh_token"] = refresh_token.token
        data["expires"] = token.expires

    else:
        data = serializer.errors

    return Response(data)



class ListPatients(generics.ListAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]



class ListCreateTaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        patient_name = self.request.data or None
        patient = get_object_or_404(PatientProfile, user=user)
        try:
            query = Task.objects.custom_all(patient=patient)
        except Exception as e:
            return Response({"error": e}, status=404)

        return query


class UpdateDeleteRetrieveTaskView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        patient = PatientProfile.objects.get(user=user)
        return Task.objects.custom_all(patient=patient)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class SearchListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        patient = PatientProfile.objects.get(user=user)
        q = self.request.GET.get("q")
        if q is None:
            return Task.objects.none()

        qs = Task.objects.search(q, patient)
        return qs


class FavoritesListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        patient = PatientProfile.objects.get(user=user)
        qs = Task.objects.get_favorites(patient)
        return qs


class TrashListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        patient = PatientProfile.objects.get(user=user)
        qs = Task.objects.get_trash(patient)
        return qs


class HiddenListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        patient = PatientProfile.objects.get(user=user)
        qs = Task.objects.get_hidden(patient)
        return qs



class ListAppointments(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = CreateAppointment
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        patient = get_object_or_404(PatientProfile,user=user)
        qs = qs.filter(patient=patient)
        return qs
