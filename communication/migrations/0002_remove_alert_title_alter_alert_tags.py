# Generated by Django 4.2 on 2023-10-11 22:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("communication", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="alert",
            name="title",
        ),
        migrations.AlterField(
            model_name="alert",
            name="tags",
            field=models.CharField(max_length=15, null=True),
        ),
    ]