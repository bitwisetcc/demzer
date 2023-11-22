from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateField,
    ForeignKey,
    IntegerChoices,
    Model,
    PositiveSmallIntegerField,
    TextChoices,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from management.models import Classroom, Subject


class Assessment(Model):
    class Kinds(TextChoices):
        ACTIVITY = "A", _("Atividade")
        TEST = "T", _("Prova")

    title = CharField(max_length=60, default="Atividade")
    subject = ForeignKey(Subject, SET_NULL, null=True)
    day = DateField()
    classroom = ForeignKey(Classroom, CASCADE)
    division = PositiveSmallIntegerField(null=True)
    bimester = PositiveSmallIntegerField()
    weight = PositiveSmallIntegerField(default=1)
    teacher = ForeignKey(User, SET_NULL, null=True, related_name="assessments")
    kind = CharField(max_length=1, choices=Kinds.choices, default=Kinds.ACTIVITY)
    content = TextField()

    def past(self):
        return date.today() > self.day

    def json(self):
        return {
            "pk": self.pk,
            "title": self.title,
            "subject": self.subject.name,
            "day": str(self.day.strftime("%d/%m/%Y")),
            "weight": self.weight,
            "content": self.content,
            "bimester": self.bimester,
            "kind": self.get_kind_display(),
        }

    def weekday(self):
        return settings.WEEKDAYS[self.day.weekday()]

    class Meta:
        ordering = ["day"]


class Grade(Model):
    class Gradings(IntegerChoices):
        I = 0, "I"
        R = 1, "R"
        B = 2, "B"
        MB = 3, "MB"

    assessment = ForeignKey(Assessment, SET_NULL, null=True)
    student = ForeignKey(User, CASCADE)
    value = PositiveSmallIntegerField(choices=Gradings.choices, default=Gradings.R)
    justification = TextField(null=True)


class Mention(Model):
    class Categories(TextChoices):
        BIMESTER = "B", _("Bimestre")
        COUNCIL = "C", _("Conselho")
        FINAL = "F", _("Final")

    class Gradings(IntegerChoices):
        I = 0, "I"
        R = 1, "R"
        B = 2, "B"
        MB = 3, "MB"

    value = PositiveSmallIntegerField(choices=Gradings.choices, default=Gradings.B)
    student = ForeignKey(User, CASCADE, related_name="mentions")
    teacher = ForeignKey(User, SET_NULL, null=True, related_name="mentions_sent")
    bimester = PositiveSmallIntegerField()
    category = CharField(
        max_length=1, choices=Categories.choices, default=Categories.BIMESTER
    )
    subject = ForeignKey(Subject, SET_NULL, related_name="mentions", null=True)
    justification = CharField(max_length=127, default="")
