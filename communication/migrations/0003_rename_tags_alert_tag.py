# Generated by Django 4.2 on 2023-10-11 22:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("communication", "0002_remove_alert_title_alter_alert_tags"),
    ]

    operations = [
        migrations.RenameField(
            model_name="alert",
            old_name="tags",
            new_name="tag",
        ),
    ]