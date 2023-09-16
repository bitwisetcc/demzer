# Generated by Django 4.2 on 2023-09-16 19:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("management", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Relative",
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
                ("name", models.CharField(max_length=60, unique=True)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Member",
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
                (
                    "contact_email",
                    models.EmailField(
                        default="john.doe@email.com", max_length=254, unique=True
                    ),
                ),
                ("rg", models.CharField(default="", max_length=9, unique=True)),
                ("cpf", models.CharField(default="", max_length=11, unique=True)),
                ("phone", models.IntegerField(default=0, unique=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("M", "Masculino"),
                            ("F", "Feminino"),
                            ("NB", "Não Binário"),
                        ],
                        default="M",
                        max_length=2,
                    ),
                ),
                (
                    "public_schooling",
                    models.CharField(
                        choices=[
                            ("C", "Completo"),
                            ("N", "Nenhuma"),
                            ("E", "Ensino Primário"),
                            ("M", "Ensino Fundamental"),
                            ("H", "Ensino Médio"),
                        ],
                        default="M",
                        max_length=1,
                        null=True,
                    ),
                ),
                ("birthdate", models.DateField(default=datetime.date(2008, 1, 1))),
                ("afro", models.BooleanField(default=False)),
                ("indigenous", models.BooleanField(default=False)),
                ("deficiencies", models.CharField(max_length=50, null=True)),
                (
                    "civil_state",
                    models.CharField(
                        choices=[
                            ("S", "Solteiro"),
                            ("M", "Casado"),
                            ("D", "Divorciado"),
                            ("W", "Viúvo"),
                        ],
                        default="S",
                        max_length=1,
                    ),
                ),
                ("cep", models.CharField(default="", max_length=8)),
                ("city", models.CharField(default="São Caetano do Sul", max_length=60)),
                ("neighborhood", models.CharField(max_length=40)),
                ("street", models.CharField(max_length=40)),
                ("street_number", models.IntegerField(default=1)),
                ("complement", models.CharField(max_length=20, null=True)),
                ("status", models.CharField(max_length=10, null=True)),
                ("division", models.CharField(max_length=1, null=True)),
                (
                    "classroom",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="students",
                        to="management.classroom",
                    ),
                ),
                ("relatives", models.ManyToManyField(to="core.relative")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "usuário",
                "verbose_name_plural": "usuários",
            },
        ),
    ]
