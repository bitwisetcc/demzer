# Generated by Django 4.2 on 2025-03-16 03:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_member_division"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="birthdate",
            field=models.DateField(default=datetime.date(2010, 1, 1)),
        ),
    ]
