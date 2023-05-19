from django.db import IntegrityError
from django.http import (
    HttpResponse,
    HttpRequest,
    JsonResponse,
    Http404,
)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
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


def index(request: HttpRequest):
    return render(
        request,
        "core/home.html",
        {"users": [user.json() for user in Member.objects.all()]},
    )


def login_user(request: HttpRequest):
    if request.method == "POST":
        user_id = request.POST["user-id"]
        password = request.POST["password"]
        username = User.objects.get(pk=user_id).username
        print(username)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            # Error message
            return redirect("login")
    else:
        return render(request, "core/login.html", {"no_links": True})


# TODO: Create actual emails + prevent email duplication
def enroll(request: HttpRequest):
    if request.method == "POST":
        username = request.POST["username"].strip()
        first_name = username.split()[0]
        last_name = username.split()[-1]
        birthdate = datetime.strptime(request.POST["birthdate"], "%Y-%m-%d").date()

        try:
            distance = int(request.POST["distance"])
        except ValueError:
            distance = None

        try:
            user = User.objects.create_user(
                username=username, 
                email=EMAIL_PATTERN.format(first_name.lower(), last_name.lower()), 
                password=first_name + last_name + str(birthdate.year),
            )
    
            user.save()
        except IntegrityError as err:
            raise Http404(f"Nome de usuário ou e-mail já existe: {err}")


        # try:
        profile = Member.objects.create(
            user=user,
            contact_email=request.POST["contact-email"],
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

        print("good 4")

        guardian = Relative.objects.create(  # TODO: Check if relative already exists
            name=request.POST["name-guardian"],
            email=request.POST["email-guardian"],
            phone=re.sub(r"[^0-9]+", "", request.POST["phone-guardian"]),
        )

        print("good 5")

        profile.save()
        profile.relatives.add(guardian)
        profile.save()

        print("good 6")

        return HttpResponse("haiii")
        # except:
            # TODO: Actually handle errors
            # return HttpResponse("something nice (◕ᴗ◕✿)")
    else:
        context = {
            "birthdate": DEFAULT_BIRTHDATE,
            "country": DEFAULT_COUNTRY,
            "state": DEFAULT_STATE,
            "city": DEFAULT_CITY,
        }
        return render(request, "core/enroll.html", context)


def detail(request: HttpRequest, user_id: int):
    return JsonResponse(Member.objects.get(id=user_id))


def all_users(request: HttpRequest):
    return HttpResponse(Member.objects.first())


def all_students(request: HttpRequest):
    """
    (Eventually) Returns all users a teacher has a relationship with
    or students from the same class as the one who made the request.
    """

    everyone = [
        user.serialize_json()
        for user in Member.objects.all()
        if user.user_type == Member.UserTypes.STUDENT
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
        teacher=Member.objects.get(pk=body["teacher"]),
        subject=Subject.objects.get(slug=body["subject"]),
        day=body["day"],
        order=body["order"],
    ).save()

    return HttpResponse(":D")
