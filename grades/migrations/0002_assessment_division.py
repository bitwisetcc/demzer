# Generated by Django 4.2 on 2023-10-30 20:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("grades", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessment",
            name="division",
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
