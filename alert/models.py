from django.db.models import Model, FileField, ForeignKey, ManyToManyField, PROTECT
from django.db.models.fields import TextField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Alert(Model):
    emiter = ForeignKey(User, PROTECT)
    recipients = ManyToManyField(User, related_name="alerts")
    description = TextField()
    attachment = FileField(upload_to="uploads/alert_attachments/%Y/")
