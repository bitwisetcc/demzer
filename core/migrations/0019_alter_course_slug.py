
# Generated by Django 4.2 on 2023-08-21 12:40

# Generated by Django 4.2 on 2023-08-20 15:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0018_course_duration_course_info"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="slug",
            field=models.SlugField(default="-", max_length=2, unique=True),
        ),
    ]
