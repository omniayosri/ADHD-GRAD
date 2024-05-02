from django.apps import AppConfig


class PatientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "patients"

    def ready(self) -> None:
        from doctors.signals import create_auth_token
