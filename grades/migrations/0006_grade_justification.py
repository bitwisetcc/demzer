# Generated by Django 4.2 on 2023-11-06 20:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("grades", "0005_alter_assessment_options_assessment_weight"),
    ]

    operations = [
        migrations.AddField(
            model_name="grade",
            name="justification",
            field=models.TextField(null=True),
        ),
    ]
