# Generated by Django 4.2 on 2023-07-10 20:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_course_time_alter_member_country_of_origin_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="subject",
            name="description",
            field=models.CharField(max_length=127, null=True),
        ),
    ]
