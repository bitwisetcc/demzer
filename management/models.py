import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.db import OperationalError
from django.db.models import (
    CASCADE,
    SET_NULL,
    ForeignKey,
    IntegerChoices,
    ManyToManyField,
    Model,
    TextChoices,
    TextField,
    DateField,
    CharField,
    FloatField,
    IntegerField,
    SlugField,
    PositiveSmallIntegerField,
)
from django.forms import ValidationError
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from rolepermissions.checkers import has_role

from core.roles import Teacher


class Subject(Model):
    """
    The subject of a class; what the teacher is talking about.
    """

    name = CharField(max_length=60)
    slug = CharField(max_length=5)
    description = CharField(max_length=127, null=True)

    def __str__(self) -> str:
        return self.slug

    class Meta:
        ordering = ["name"]
        verbose_name = _("matéria")
        verbose_name_plural = _("matérias")

    # ...


class Course(Model):
    """
    The group of students that spend their time together. They go from room to room together etc.
    The naming doesn't imply it, but there can be many 'generations' of a course.
    Ex: 1st, 2nd and 3rd Philosophy and Sociology.
    """

    class Timing(TextChoices):
        MORNING = "M", _("Manhã")
        EVENING = "E", _("Tarde")
        NIGHT = "N", _("Noite")

    name = CharField(max_length=60)
    slug = SlugField(max_length=2, default="-", unique=True)
    subjects = ManyToManyField(Subject)
    time = CharField(max_length=1, choices=Timing.choices, default=Timing.MORNING)
    coordinator = ForeignKey(User, SET_NULL, null=True, related_name="courses")
    info = TextField(null=True)
    duration = FloatField(default=3)

    class Meta:
        verbose_name = _("curso")
        verbose_name_plural = _("cursos")

    def __str__(self) -> str:
        return self.slug


class Classroom(Model):
    course = ForeignKey(Course, SET_NULL, related_name="classrooms", null=True)
    year = IntegerField(default=2023)

    def __str__(self) -> str:
        return self.course.slug + str(self.year)


class Programming(Model):
    """
    A class that appears on the calendar. Not to be confused with `Course`.
    """

    class Days(IntegerChoices):
        MONDAY = 0, _("Segunda")
        TUESDAY = 1, _("Terça")
        WEDNESDAY = 2, _("Quarta")
        THURSDAY = 3, _("Quinta")
        FRIDAY = 4, _("Sexta")

    classroom = ForeignKey(Classroom, CASCADE, related_name="programmings", null=True)
    teacher = ForeignKey(User, SET_NULL, null=True, related_name="programmings")
    group = PositiveSmallIntegerField(null=True)
    subject = ForeignKey(Subject, SET_NULL, related_name="programmings", null=True)
    day = PositiveSmallIntegerField(choices=Days.choices, default=Days.MONDAY)
    order = PositiveSmallIntegerField()

    def create(
        request: HttpRequest,
        classroom: Classroom,
        teacher_name: str,
        subject_pk: int,
        group: int = None,
    ):
        try:
            day = Programming.Days.choices[int(request.POST.get("day"))][0]
            time = request.POST.get("time")
            teacher = User.objects.get(
                username__startswith=teacher_name, groups__name__in=["Teacher"]
            )
            subject = Subject.objects.get(pk=subject_pk)

            if not has_role(teacher, Teacher):
                raise PermissionError(teacher.username)

            # avoid teacher overbooking
            check = Programming.objects.filter(teacher=teacher, order=time, day=day)
            if check.count() > 0 and check.first().classroom != classroom:
                raise ValidationError(
                    "Professor {} já tem aula nesse horário".format(teacher_name)
                )

            # edit programmings
            previous = Programming.objects.filter(
                classroom=classroom, order=time, day=day
            )
            if group is None:
                previous.delete()
            else:
                previous.filter(group=None).delete()

            return Programming.objects.create(
                classroom=classroom,
                teacher=teacher,
                group=group,
                subject=subject,
                day=day,
                order=time,
            )

        except User.DoesNotExist as exc:
            messages.error(request, "Professor não encontrado")
        except User.MultipleObjectsReturned as exc:
            messages.error(request, "Mais de um '{}' encontrado".format(teacher_name))
        except PermissionError as exc:
            messages.error(request, "Usuário '{}' não é um professor".format(exc))
        except ValidationError as exc:
            messages.error(request, exc)
        except Subject.DoesNotExist as exc:
            messages.error(request, "Matéria não encontrada")
        except OperationalError as err:
            messages.error(
                request, "Falha ao conectar com a BD: {}".format(err.args[0])
            )

    def json(self):
        return {
            "pk": self.pk,
            "classroom": self.classroom.__str__(),
            "teacher": self.teacher.username,
            "group": self.group,
            "subjectSlug": self.subject.slug,
            "subject": self.subject.name,
            "subjectPk": self.subject.pk,
            "day": self.day,
            "order": self.order,
        }

    def json_str(self):
        return json.dumps(
            {
                "pk": self.pk,
                "classroom": self.classroom.__str__(),
                "teacher": self.teacher.username,
                "group": self.group,
                "subjectSlug": self.subject.slug,
                "subject": self.subject.name,
                "subjectPk": self.subject.pk,
                "day": self.day,
                "order": self.order,
            }
        )

    class Meta:
        ordering = ["group"]
        verbose_name = _("classe")
        verbose_name_plural = _("classes")

    def __str__(self) -> str:
        return "{}".format(self.subject.__str__())


class Lesson(Model):
    programming = ForeignKey(Programming, SET_NULL, null=True)
    day = DateField(auto_created=True)


class Attendance(Model):
    student = ForeignKey(User, CASCADE)
    lesson = ForeignKey(Lesson, SET_NULL, null=True)
