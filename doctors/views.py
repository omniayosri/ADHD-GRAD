from rest_framework.response import Response
from rest_framework.decorators import api_view
from oauth2_provider.models import AccessToken, RefreshToken
from rest_framework import status
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from datetime import datetime, timedelta


from .serializers import (
    DoctorRegistration,
    DoctorRetrieveSerializer,
    DoctorFreeTimeSlotSerializer,
    CreateAppointment,
)

from .models import DoctorProfile, FreeTimeSlot, Appointment
from patients.models import PatientProfile


@api_view(["POST"])
def user_register_view(request):
    serializer = DoctorRegistration(data=request.data)

    data = {}

    if serializer.is_valid():
        specialize = serializer.validated_data["specialize"]
        contact = serializer.validated_data["contact"]
        address = serializer.validated_data["address"]
        experiance = serializer.validated_data["experiance"]
        birth_date = serializer.validated_data["birth_date"]
        photo = request.FILES.get("photo")

        user = serializer.save()
        DoctorProfile.objects.create(
            user=user,
            specialize=specialize,
            contact=contact,
            address=address,
            experiance=experiance,
            birth_date=birth_date,
            photo=photo,
        )

        data["response"] = "Account for Doctor has been created"
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


class UpdateDeleteRetrieveDoctorView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "email"

    def get_queryset(self):
        email = self.kwargs.get("email")
        user = get_object_or_404(User, email=email)
        if user == self.request.user or self.request.user.is_superuser:
            doctor_profile = get_object_or_404(DoctorProfile, user=user)
            # print(doctor_profile)
            return doctor_profile
        else:
            raise NotFound("You are not authorized")

    def get_object(self):
        return self.get_queryset()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = get_object_or_404(User, email=instance.user.email)
        self.perform_destroy(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = get_object_or_404(User, email=instance.user.email)
        data = request.data

        try:
            for key, value in data.items():
                if key not in ["username", "email"]:
                    setattr(instance, key, value)
                elif key in ["username", "email"]:
                    setattr(user, key, value)

            instance.save()
            user.save()
        except Exception as e:
            return Response({"error": e})

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ListDoctorsView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["POST"])
def logout_user(request):
    try:
        token = request.headers.get("Authorization", "")[7:]
        access_token = AccessToken.objects.get(token=token)
        user = access_token.user
        access_token.delete()
        refresh_token = RefreshToken.objects.get(user=user)
        refresh_token.delete()

        return Response(
            {"Message": "You are successfully logged out"}, status=status.HTTP_200_OK
        )
    except AccessToken.DoesNotExist:
        return Response({"Message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"Message": e})


class CreateListFreeSlot(generics.ListCreateAPIView):
    queryset = FreeTimeSlot.objects.all()
    serializer_class = DoctorFreeTimeSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        doctor = DoctorProfile.objects.get(user=user)
        qs = qs.filter(doctor=doctor)
        return qs

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        start_string = data["start_time"]
        end_string = data["end_time"]
        date_format = "%Y-%m-%dT%I:%M %p"
        start_obj = datetime.strptime(start_string, date_format)
        end_obj = datetime.strptime(end_string, date_format)
        data["start_time"] = start_obj
        data["end_time"] = end_obj
        user = request.user
        doctor = get_object_or_404(DoctorProfile, id=data["doctor"])
        if doctor.user == user:

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(
                {"Error": "You're not allowed to do this"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreateListAppointment(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = CreateAppointment
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        doctor = get_object_or_404(DoctorProfile, user=user)
        qs = qs.filter(doctor=doctor)
        return qs

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        date_format = date_format = "%Y-%m-%dT%I:%M %p"
        data["date_time"] = datetime.strptime(data["date_time"], date_format)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        doctor = data["doctor"]
        appointment_time = data["date_time"]
        print(appointment_time)
        user = request.user
        doctor = get_object_or_404(DoctorProfile, id=data["doctor"]) or None
        patient = get_object_or_404(PatientProfile, id=data["patient"]) or None

        if doctor.user == user or patient.user == user:

            free_slot = FreeTimeSlot.objects.filter(
                doctor=doctor,
                start_time__lte=appointment_time,
                end_time__gte=appointment_time,
            ).exists()

            # print('=====================',free_slot)

            if free_slot:
                # Check if there isn't already another appointment at the same time for the doctor
                if not Appointment.objects.filter(
                    doctor=doctor,
                    date_time=appointment_time,
                    date_time__lte=(appointment_time + timedelta(minutes=30)),
                ).exists():
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    print("Appointment successfully created.")
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED, headers=headers
                    )
                else:
                    return Response(
                        {
                            "Error": "Another appointment already exists at this time for this doctor."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"Error": "There's no time for the doctor in this time"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(
                {"Error": "You're not allowed to do this"},
                status=status.HTTP_400_BAD_REQUEST,
            )
