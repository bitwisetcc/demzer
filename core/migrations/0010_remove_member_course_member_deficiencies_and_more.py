# Generated by Django 4.2 on 2023-08-04 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_remove_member_distance_member_picture"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="course",
        ),
        migrations.AddField(
            model_name="member",
            name="deficiencies",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="member",
            name="status",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.CreateModel(
            name="Classroom",
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
                (
                    "course",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="classroom",
                        to="core.course",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="member",
            name="classrooms",
            field=models.ManyToManyField(related_name="students", to="core.classroom"),
        ),
    ]
