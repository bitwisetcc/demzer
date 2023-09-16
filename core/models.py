from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    EmailField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    OneToOneField,
    TextChoices,
)
from django.utils.translation import gettext_lazy as _

from management.models import Classroom


class Relative(Model):
    name = CharField(max_length=60, unique=True)
    email = EmailField()
    phone = IntegerField(default=0)


class Member(Model):
    """
    The main character of the system. Can be a student, a teacher or an employee.
    """

    class Genders(TextChoices):
        MASCULINE = "M", _("Masculino")
        FEMININE = "F", _("Feminino")
        NON_BINARY = "NB", _("Não Binário")

    class PublicSchoolingTypes(TextChoices):
        FULL = "C", _("Completo")
        NONE = "N", _("Nenhuma")
        ELEMENTARY = "E", _("Ensino Primário")
        MIDDLE = "M", _("Ensino Fundamental")
        HIGH = "H", _("Ensino Médio")

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

    user = OneToOneField(User, CASCADE, related_name="profile", unique=True)
    contact_email = EmailField(default="john.doe@email.com", unique=True)

    rg = CharField(default="", max_length=9, unique=True)
    cpf = CharField(default="", max_length=11, unique=True)
    phone = IntegerField(default=0, unique=True)
    gender = CharField(choices=Genders.choices, default=Genders.MASCULINE, max_length=2)
    public_schooling = CharField(
        choices=PublicSchoolingTypes.choices,
        default=PublicSchoolingTypes.MIDDLE,
        max_length=1,
        null=True,
    )
    birthdate = DateField(default=settings.DEFAULT_BIRTHDATE)
    afro = BooleanField(default=False)
    indigenous = BooleanField(default=False)
    deficiencies = CharField(null=True, max_length=50)
    civil_state = CharField(
        choices=CivilStates.choices, default=CivilStates.SINGLE, max_length=1
    )

    cep = CharField(default="", max_length=8)
    city = CharField(max_length=60, default=settings.DEFAULT_CITY)
    neighborhood = CharField(max_length=40)
    street = CharField(max_length=40)
    street_number = IntegerField(default=1)
    complement = CharField(max_length=20, null=True)

    relatives = ManyToManyField(Relative)
    classroom = ForeignKey(Classroom, SET_NULL, related_name="students", null=True)
    status = CharField(null=True, max_length=10)
    division = CharField(max_length=1, null=True)

    def json(self):
        return {
            "rm": self.user.pk,
            "username": self.user.username,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.user.email,
            "rg": self.rg,
            "cpf": self.cpf,
            "is_staff": self.user.is_staff,
        }

    class Meta:
        verbose_name = _("usuário")
        verbose_name_plural = _("usuários")

    def __str__(self):
        return "{} {} ({})".format(
            self.user.first_name,
            self.user.last_name,
            self.user.pk,
        )


"""
- is_staff ?
- is_active ? -> celery

New TO-DOs
- Deal with failed students
? Generating emails 😵‍💫
- Events (signals) for holidays, awareness days, meetings etc.
- Yearly checksums:
    Archive students that graduated n years ago
    Control checksums with a key variable (boolean)

"""
