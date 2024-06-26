# Generated by Django 5.0.1 on 2024-02-13 16:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CreateNewTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("purpose", models.CharField(max_length=250)),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "priority",
                    models.CharField(
                        choices=[("LW", "Low"), ("MD", "Medium"), ("HG", "High")],
                        max_length=2,
                    ),
                ),
                ("description", models.TextField()),
                ("reminder", models.BooleanField(default=False)),
                ("trash", models.BooleanField(default=False)),
                ("favorite", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_tasks",
                        to="patients.patientprofile",
                    ),
                ),
            ],
        ),
    ]
