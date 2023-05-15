from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseBadRequest,
    JsonResponse,
    Http404,
)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import datetime
import json
import re

from core.models import *
from backend.settings import (
    DEFAULT_COUNTRY,
    DEFAULT_STATE,
    DEFAULT_CITY,
    DEFAULT_BIRTHDATE,
    EMAIL_PATTERN,
)


def default_value(field):
    return User._meta.get_field(field).get_default()


def index(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, "core/home.html")  # Not implemented yet
    else:
        return render(request, "core/home.html")


def login(request: HttpRequest):
    return render(request, "core/login.html")


# TODO: Create actual emails + prevent email duplication
def enroll(request: HttpRequest):
    if request.method == "POST":
        # try:
            if len(re.sub(r"[a-zA-z\s]+", "", request.POST["username"])):
                return HttpResponseBadRequest(
                    "Nome de usuário deve conter apenas letras"
                )

            # TODO: Validate the rest

            first_name = request.POST["username"].split()[0]
            last_name = request.POST["username"].split()[-1]
            birthdate = datetime.strptime(request.POST["birthdate"], "%Y-%m-%d").date()
            try:
                distance = int(request.POST["distance"])
            except ValueError:
                distance = None

            user = User.objects.create(
                username=request.POST["username"],
                first_name=first_name,
                last_name=last_name,
                contact_email=request.POST["contact-email"],
                email=EMAIL_PATTERN.format(first_name, last_name),
                password=first_name + last_name + str(birthdate.year),
                phone=re.sub(r"[^0-9]+", "", request.POST["phone"]),
                birthdate=birthdate,
                gender=request.POST["gender"],
                rg=request.POST["rg"],
                cpf=request.POST["cpf"],
                public_schooling=request.POST["public-schooling"],
                afro="afro" in request.POST,
                civil_state=request.POST["civil-state"],
                natural_state=request.POST["natural-state"],
                natural_city=request.POST["natural-city"],
                nationality=request.POST["nationality"],
                country_of_origin=request.POST["country-of-origin"],
                cep=request.POST["cep"],
                city=request.POST["residence-city"],
                neighborhood=request.POST["neighborhood"],
                street=request.POST["street"],
                street_number=request.POST["street-number"],
                complement=request.POST["complement"],
                distance=distance,
            )

            guardian = Relative.objects.create(
                name=request.POST["name-guardian"],
                email=request.POST["email-guardian"],
                phone=request.POST["phone-guardian"],
            )

            user.save()
            user.relatives.add(guardian)

            return HttpResponse("haiii")
        # except:
        #     return HttpResponse("fudeu")
    else:
        context = {
            "birthdate": DEFAULT_BIRTHDATE,
            "country": DEFAULT_COUNTRY,
            "state": DEFAULT_STATE,
            "city": DEFAULT_CITY,
        }
        return render(request, "core/enroll.html", context)


def detail(request: HttpRequest, user_id: int):
    return JsonResponse(User.objects.get(id=user_id))


def all_users(request: HttpRequest):
    return HttpResponse(User.objects.first())


def all_students(request: HttpRequest):
    """
    (Eventually) Returns all users a teacher has a relationship with
    or students from the same class as the one who made the request.
    """

    everyone = [
        user.serialize_json()
        for user in User.objects.all()
        if user.user_type == User.UserTypes.STUDENT
    ]

    return JsonResponse({"total": len(everyone), "users": everyone})


@csrf_exempt
@require_POST
def create_subject(request: HttpRequest):
    body = json.loads(request.body.decode())
    Subject(name=body["name"], slug=body["slug"]).save()
    return HttpResponse(":D")


@csrf_exempt
@require_POST
def create_course(request: HttpRequest):
    body = json.loads(request.body.decode())
    course = Course(name=body["name"], slug=body["slug"])
    course.save()

    _subjects = [Subject.objects.get(slug=s) for s in body["subjects"]]
    course.subjects.add(*_subjects)
    course.save()

    return HttpResponse(":D")


@csrf_exempt
@require_POST
def create_class(request: HttpRequest):
    body = json.loads(request.body.decode())

    Class(
        course=Course.objects.get(slug=body["course"]),
        student_group=body["student_group"] or None,
        teacher=User.objects.get(pk=body["teacher"]),
        subject=Subject.objects.get(slug=body["subject"]),
        day=body["day"],
        order=body["order"],
    ).save()

    return HttpResponse(":D")
