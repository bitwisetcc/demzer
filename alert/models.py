from django.db.models import (
    Model,
    FileField,
    ForeignKey,
    CharField,
    PROTECT,
)
from django.db.models.fields import TextField, DateTimeField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Alert(Model):
    emiter = ForeignKey(User, PROTECT)
    date = DateTimeField(auto_created=True, null=True)
    title = CharField(max_length=30, default="Denúncia genérica")
    tags = CharField(max_length=50, null=True)
    description = TextField()
    attachment = FileField(upload_to="uploads/alert_attachments/%Y/")
