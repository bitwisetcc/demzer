from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateField,
    ForeignKey,
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
    kind = CharField(max_length=1, choices=Kinds.choices, default=Kinds.ACTIVITY)
    content = TextField()

    def json(self):
        return {
            "title": self.title,
            "subject": self.subject.name,
            "day": str(self.day),
            "weight": self.weight,
            "content": self.content,
            "bimester": self.bimester,
            "kind": self.kind
        }

    class Meta:
        ordering = ["day"]


class Grade(Model):
    assessment = ForeignKey(Assessment, SET_NULL, null=True)
    student = ForeignKey(User, CASCADE)
    value = PositiveSmallIntegerField()


class Mention(Model):
    class Categories(TextChoices):
        BIMESTER = "B", _("Bimestre")
        COUNCIL = "C", _("Conselho")
        FINAL = "F", _("Final")

    value = PositiveSmallIntegerField()
    student = ForeignKey(User, CASCADE, related_name="mentions")
    teacher = ForeignKey(User, SET_NULL, null=True, related_name="mentions_sent")
    bimester = PositiveSmallIntegerField()
    category = CharField(
        max_length=1, choices=Categories.choices, default=Categories.BIMESTER
    )
    justification = CharField(max_length=127, default="")
