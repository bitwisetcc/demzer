# Generated by Django 4.2 on 2023-11-07 01:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("management", "0002_alter_subject_options_alter_course_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programming",
            name="classroom",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="programmings",
                to="management.classroom",
            ),
        ),
        migrations.AlterField(
            model_name="programming",
            name="subject",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="programmings",
                to="management.subject",
            ),
        ),
        migrations.AlterField(
            model_name="programming",
            name="teacher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="programmings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
