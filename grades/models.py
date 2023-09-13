from email.policy import default
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
    attachement = FileField(upload_to="assessments/attachements")
    content = TextField()


class Grade(Model):
    value = PositiveSmallIntegerField()
    student = ForeignKey(User, CASCADE)
    assessment = ForeignKey(Assessment, SET_NULL)


class Mention(Model):
    value = PositiveSmallIntegerField()
    student = ForeignKey(User, CASCADE)
    teacher = ForeignKey(User, SET_NULL)
    bimester = PositiveSmallIntegerField()
    category = CharField(max_length=1, default="B") # TODO: use an enum: bimester, final, council ...
    justification = CharField(max_length=127, default="")


