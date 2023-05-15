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
    BooleanField,
    FloatField,
    IntegerField,
)
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.core.validators import RegexValidator
from backend.settings import (
    DEFAULT_COUNTRY,
    DEFAULT_STATE,
    DEFAULT_CITY,
    DEFAULT_BIRTHDATE,
)


@deconstructible
class NameValidator(RegexValidator):
    regex = r"^[\w\.?\s]+"
    message = _("Digite um nome válido. Apenas letras e ponto")
    flags = 0


class Relative(Model):
    name = CharField(max_length=60, unique=True)
    email = EmailField()
    phone = CharField(max_length=11)


class User(AbstractUser):
    """
    The main character of the system. Can be a student, a parent, a teacher or an employee.
    """

    class Genders(TextChoices):
        MASCULINE = "M", _("Masculino")
        FEMININE = "F", _("Feminino")
        NON_BINARY = "NB", _("Não Binário")

    class UserTypes(TextChoices):
        STUDENT = "0", _("Aluno")
        TEACHER = "1", _("Professor")
        EMPLOYEE = "2", _("Funcionário")
        ADMIN = "3", _("Administrador")

    class PublicSchoolingTypes(TextChoices):
        FULL = "C", _("Completo")
        NONE = "N", _("Nenhuma")
        ELEMENTARY = "E", _("Ensino Primário")
        MIDDLE = "M", _("Ensino Fundamental")
        HIGH = "H", _("Ensino Média")

    class CivilStates(TextChoices):
        SINGLE = "S", _("Solteiro")
        MARRIED = "M", _("Casado")
        DIVORCED = "D", _("Divorciado")
        WIDOWED = "W", _("Viúvo")

    class States(TextChoices):
        RO = "RO"
        AC = "AC"
        AM = "AM"
        RR = "RR"
        PA = "PA"
        AP = "AP"
        TO = "TO"
        MA = "MA"
        PI = "PI"
        CE = "CE"
        RN = "RN"
        PB = "PB"
        PE = "PE"
        AL = "AL"
        SE = "SE"
        BA = "BA"
        MG = "MG"
        ES = "ES"
        RJ = "RJ"
        SP = "SP"
        PR = "PR"
        SC = "SC"
        RS = "RS"
        MS = "MS"
        MT = "MT"
        GO = "GO"
        DF = "DF"

    name_validator = NameValidator()

    email = EmailField(unique=True)
    contact_email = EmailField(default="john.doe@email.com")
    username = CharField(
        max_length=100,
        help_text=_("Obrigatório. 100 ou menos. Apenas letras e ponto"),
        validators=[name_validator],
        unique=True,
    )

    rg = IntegerField(default=0)
    cpf = IntegerField(default=0)
    phone = IntegerField(default=0)
    gender = CharField(choices=Genders.choices, default=Genders.MASCULINE, max_length=2)
    public_schooling = CharField(
        choices=PublicSchoolingTypes.choices,
        default=PublicSchoolingTypes.MIDDLE,
        max_length=1,
    )
    birthdate = DateField(default=DEFAULT_BIRTHDATE)
    afro = BooleanField(default=False)

    natural_state = CharField(
        choices=States.choices, default=DEFAULT_STATE, max_length=2
    )
    natural_city = CharField(default=DEFAULT_CITY, max_length=50)
    nationality = CharField(default=DEFAULT_COUNTRY, max_length=40)
    country_of_origin = CharField(default=DEFAULT_COUNTRY, max_length=40)
    civil_state = CharField(
        choices=CivilStates.choices, default=CivilStates.SINGLE, max_length=1
    )

    cep = IntegerField(default=0)
    city = CharField(max_length=60, default=DEFAULT_CITY)
    neighborhood = CharField(max_length=40)
    street = CharField(max_length=40)
    street_number = IntegerField(default=1)
    complement = CharField(max_length=20)
    distance = FloatField(default=0)

    relatives = ManyToManyField(Relative)

    course = ForeignKey("Course", PROTECT, related_name="students", null=True)

    user_type = SlugField(
        choices=UserTypes.choices, default=UserTypes.STUDENT, max_length=1
    )

    def get_full_name(self):
        return self.username.strip()

    def get_short_name(self):
        return self.username.split()[0]

    class Meta:
        abstract = False
        verbose_name = _("usuário")
        verbose_name_plural = _("usuários")


class Subject(Model):
    """
    The subject of a class; what the teacher is talking about.
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
