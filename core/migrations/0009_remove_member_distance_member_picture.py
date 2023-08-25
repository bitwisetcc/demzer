# Generated by Django 4.2 on 2023-07-26 01:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_alter_course_coordinator"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="distance",
        ),
        migrations.AddField(
            model_name="member",
            name="picture",
            field=models.ImageField(null=True, upload_to="users/pictures"),
        ),
    ]
