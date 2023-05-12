from django.conf import settings
from django.db.models import (
    Model,
    TextChoices,
    ForeignKey,
    ManyToManyField,
    PROTECT,
    CASCADE,
)
from django.db.models.fields import (
    PositiveSmallIntegerField,
    CharField,
    DateField,
    EmailField,
    SlugField,
)
from django.contrib.auth.models import AbstractUser
from django.forms import BooleanField, IntegerField
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.core.validators import RegexValidator


@deconstructible
class NameValidator(RegexValidator):
    regex = r"^[\w\.?\s]+"
    message = _("Digite um nome válido. Apenas letras e ponto")
    flags = 0


class User(AbstractUser):
    """
    The main character of the system. Can be a student, a parent, a teacher or an employee.
    """

    class GenderTypes(TextChoices):
        MASCULINE = "M", _("Masculino")
        FEMININE = "F", _("Feminino")
        NON_BINARY = "NB", _("Não Binário")

    class UserTypes(TextChoices):
        STUDENT = "0", _("Aluno")
        GUARDIAN = "1", _("Responsável")
        TEACHER = "2", _("Professor")
        EMPLOYEE = "3", _("Funcionário")

    name_validator = NameValidator()

    email = EmailField(_("Endereço de email"), unique=True)
    username = CharField(
        max_length=100,
        help_text=_("Obrigatório. 100 ou menos. Apenas letras e ponto"),
        validators=[name_validator],
        unique=True
    )

    rg = CharField(max_length=9, null=True)
    cpf = CharField(max_length=11, null=True) # validate
    phone = CharField(max_length=11)
    gender = CharField(null=True, choices=GenderTypes.choices, max_length=2)
    birthdate = DateField(blank=True)
    afro = BooleanField()
    # naturalidade = 

    course = ForeignKey("Course", PROTECT, related_name="students", null=True, default=None)
    relatives = ManyToManyField("self")
    user_type = SlugField(choices=UserTypes.choices, default=UserTypes.STUDENT, max_length=1)

    def get_full_name(self):
        return self.username.strip()

    def get_short_name(self):
        return self.username.split()[0]

    def serialize_json(self):
        return {"username": self.username, "email": self.email, "id": self.pk}

    class Meta:
        abstract = False
        verbose_name = _("usuário")
        verbose_name_plural = _("usuários")
        # swappable = "AUTH_USER_MODEL"


class Subject(Model):
    """
    The subject of a class; what the teacher is talking about.
    { "name": "Física" }
    """

    name = CharField(max_length=63)
    slug = CharField(max_length=5)

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name = _("matéria")
        verbose_name_plural = _("matérias")

    # ...


class Course(Model):
    """
    The group of students that spend their time together. They go from room to room together etc.
    The naming doesn't imply it, but there can be many 'generations' of a course.
    Ex: 1st, 2nd and 3rd Philosophy and Sociology.
    { "name": "2nd Information Technology", "slug": "2IT", "subjects": [...] }
    """

    name = CharField(max_length=63)
    slug = SlugField(max_length=7, default="-")
    subjects = ManyToManyField(Subject)

    class Meta:
        verbose_name = _("curso")
        verbose_name_plural = _("cursos")


class Class(Model):
    """
    A class that appears on the calendar. Not to be confused with `Course`.
    {
        "course": 232 -> "2GT",
        "teacher": 65231 -> "Thomas Arson",
        "student_group": None,
        "subject": 5 -> "Web Development"
    }
    """

    class Days(TextChoices):
        MONDAY = "MON", _("Segunda-feira")
        TUESDAY = "TUE", _("Terça-feira")
        WEDNESDAY = "WED", _("Quarta-feira")
        THURSDAY = "THU", _("Quinta-feira")
        SUNDAY = "SUN", _("Sexta-feira")

    course = ForeignKey("Course", CASCADE, related_name="+")
    teacher = ForeignKey(settings.AUTH_USER_MODEL, PROTECT)
    student_group = PositiveSmallIntegerField(null=True)
    subject = ForeignKey("Subject", PROTECT, related_name="+")
    day = CharField(max_length=15, choices=Days.choices, default=Days.MONDAY)
    order = PositiveSmallIntegerField()

    class Meta:
        verbose_name = _("classe")
        verbose_name_plural = _("classes")


class Presence(Model):
    pass


class Assessment(Model):
    pass


"""
- is_staff ?
- is_active ? -> celery

New TO-DOs
- Class editor
- Deal with failed students
? Generating emails 😵‍💫
- Events (signals) for holidays, awareness days, meetings etc.
- Yearly checksums:
    Archive students that graduated n years ago
    Control checksums with a key variable (boolean)

"""
