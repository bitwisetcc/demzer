# Generated by Django 4.2 on 2023-04-16 14:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="class",
            options={"verbose_name": "classe", "verbose_name_plural": "classes"},
        ),
        migrations.AlterModelOptions(
            name="course",
            options={"verbose_name": "curso", "verbose_name_plural": "cursos"},
        ),
        migrations.AlterModelOptions(
            name="subject",
            options={"verbose_name": "matéria", "verbose_name_plural": "matérias"},
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "usuário", "verbose_name_plural": "usuários"},
        ),
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("0", "Aluno"),
                    ("1", "Responsável"),
                    ("2", "Professor"),
                    ("3", "Funcionário"),
                ],
                default="0",
            ),
        ),
        migrations.AlterField(
            model_name="class",
            name="student_group",
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="course",
            name="name",
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name="subject",
            name="name",
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True,
                max_length=254,
                unique=True,
                verbose_name="Endereço de email",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("M", "Masculino"), ("F", "Feminino"), ("NB", "Não Binário")],
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="relatives",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
