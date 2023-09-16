from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    SET_NULL,
    DateField,
    FileField,
    ForeignKey,
    Model,
    PositiveSmallIntegerField,
    TextField,
)
from django.forms import CharField

from management.models import Classroom, Subject


class Assessment(Model):
    subject = ForeignKey(Subject, SET_NULL, null=True)
    day = DateField()
    classroom = ForeignKey(Classroom, CASCADE)
    bimester = PositiveSmallIntegerField()
    # TODO: connect to azure blobs
    content = TextField()


class Grade(Model):
    assessment = ForeignKey(Assessment, SET_NULL, null=True)
    student = ForeignKey(User, CASCADE)
    value = PositiveSmallIntegerField()


class Mention(Model):
    value = PositiveSmallIntegerField()
    student = ForeignKey(User, CASCADE, related_name="mentions")
    teacher = ForeignKey(User, SET_NULL, null=True, related_name="mentions_sent")
    bimester = PositiveSmallIntegerField()
    category = CharField(max_length=1) # TODO: use an enum: bimester, final, council ...
    justification = CharField(max_length=127)
