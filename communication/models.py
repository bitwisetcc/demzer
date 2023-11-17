from datetime import date
from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    PROTECT,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
)
from django.utils.translation import gettext_lazy as _
from management.models import Classroom, Course, Subject


class Alert(Model):
    emiter = ForeignKey(User, PROTECT)
    date = DateField(auto_created=True, null=True)
    tag = CharField(max_length=15, null=True)
    description = TextField()
    # TODO: marcar alerta como solucionado


class Announcement(Model):
    # if both date and course are None and private is False, it's a general announcement, meant for all users
    title = CharField(max_length=60, default="")
    date = DateField()
    course = ForeignKey(Course, SET_NULL, null=True)
    classroom = ForeignKey(Classroom, SET_NULL, null=True)
    private = BooleanField(default=False)
    info = TextField()
    category = CharField(max_length=15, default="*")

    def published(self):
        return date.today() >= self.date

    def category_full(self):
        match self.category:
            case "r":
                return "Reuinão"
            case "p":
                return "Palestra"
            case "a":
                return "Reposição"
            case _:
                return "Outro"

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-date"]


class Event(Model):
    # if both classroom and course are None and private is False, it's a general announcement, meant for all users
    title = CharField(max_length=80, default="")
    date = DateField()
    course = ForeignKey(Course, SET_NULL, null=True)
    classroom = ForeignKey(Classroom, SET_NULL, null=True)
    private = BooleanField(default=False)
    info = TextField()
    place = CharField(max_length=63, null=True)

    def past(self):
        return date.today() > self.date

    class Meta:
        ordering = ["-date"]


class Review(Model):
    student = ForeignKey(User, CASCADE, related_name="reviews_sent")
    teacher = ForeignKey(User, SET_NULL, null=True, related_name="reviews_recieved")
    subject = ForeignKey(Subject, SET_NULL, null=True)
    content = TextField()
