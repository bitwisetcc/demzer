# Generated by Django 4.2 on 2023-05-19 13:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Assessment",
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
            ],
        ),
        migrations.CreateModel(
            name="Course",
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
                ("name", models.CharField(max_length=63)),
                ("slug", models.SlugField(default="-", max_length=7)),
            ],
            options={
                "verbose_name": "curso",
                "verbose_name_plural": "cursos",
            },
        ),
        migrations.CreateModel(
            name="Presence",
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
            ],
        ),
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
                ("phone", models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name="Subject",
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
                ("name", models.CharField(max_length=63)),
                ("slug", models.CharField(max_length=5)),
            ],
            options={
                "verbose_name": "matéria",
                "verbose_name_plural": "matérias",
            },
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
                    models.EmailField(default="john.doe@email.com", max_length=254),
                ),
                ("rg", models.IntegerField(default=0)),
                ("cpf", models.IntegerField(default=0)),
                ("phone", models.IntegerField(default=0)),
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
                            ("H", "Ensino Média"),
                        ],
                        default="M",
                        max_length=1,
                    ),
                ),
                ("birthdate", models.DateField(default=datetime.date(2008, 1, 1))),
                ("afro", models.BooleanField(default=False)),
                ("indigenous", models.BooleanField(default=False)),
                (
                    "natural_state",
                    models.CharField(
                        choices=[
                            ("RO", "Ro"),
                            ("AC", "Ac"),
                            ("AM", "Am"),
                            ("RR", "Rr"),
                            ("PA", "Pa"),
                            ("AP", "Ap"),
                            ("TO", "To"),
                            ("MA", "Ma"),
                            ("PI", "Pi"),
                            ("CE", "Ce"),
                            ("RN", "Rn"),
                            ("PB", "Pb"),
                            ("PE", "Pe"),
                            ("AL", "Al"),
                            ("SE", "Se"),
                            ("BA", "Ba"),
                            ("MG", "Mg"),
                            ("ES", "Es"),
                            ("RJ", "Rj"),
                            ("SP", "Sp"),
                            ("PR", "Pr"),
                            ("SC", "Sc"),
                            ("RS", "Rs"),
                            ("MS", "Ms"),
                            ("MT", "Mt"),
                            ("GO", "Go"),
                            ("DF", "Df"),
                        ],
                        default="SP",
                        max_length=2,
                    ),
                ),
                (
                    "natural_city",
                    models.CharField(default="São Caetano do Sul", max_length=50),
                ),
                ("nationality", models.CharField(default="Brasil", max_length=40)),
                (
                    "country_of_origin",
                    models.CharField(default="Brasil", max_length=40),
                ),
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
                ("cep", models.IntegerField(default=0)),
                ("city", models.CharField(default="São Caetano do Sul", max_length=60)),
                ("neighborhood", models.CharField(max_length=40)),
                ("street", models.CharField(max_length=40)),
                ("street_number", models.IntegerField(default=1)),
                ("complement", models.CharField(max_length=20)),
                ("distance", models.FloatField(default=0)),
                (
                    "course",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="students",
                        to="core.course",
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
        migrations.AddField(
            model_name="course",
            name="subjects",
            field=models.ManyToManyField(to="core.subject"),
        ),
        migrations.CreateModel(
            name="Class",
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
                ("student_group", models.PositiveSmallIntegerField(null=True)),
                (
                    "day",
                    models.CharField(
                        choices=[
                            ("MON", "Segunda-feira"),
                            ("TUE", "Terça-feira"),
                            ("WED", "Quarta-feira"),
                            ("THU", "Quinta-feira"),
                            ("SUN", "Sexta-feira"),
                        ],
                        default="MON",
                        max_length=15,
                    ),
                ),
                ("order", models.PositiveSmallIntegerField()),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="core.course",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="core.subject",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "classe",
                "verbose_name_plural": "classes",
            },
        ),
    ]
