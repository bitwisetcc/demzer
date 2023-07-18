# Generated by Django 4.2 on 2023-07-10 19:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_alter_class_subject_alter_class_teacher_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="time",
            field=models.CharField(
                choices=[("M", "Manhã"), ("E", "Tarde"), ("N", "Noite")],
                default="M",
                max_length=1,
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="country_of_origin",
            field=models.CharField(default="Brasil", max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name="member",
            name="nationality",
            field=models.CharField(default="Brasil", max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name="member",
            name="natural_city",
            field=models.CharField(
                default="São Caetano do Sul", max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="natural_state",
            field=models.CharField(
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
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="public_schooling",
            field=models.CharField(
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
    ]
