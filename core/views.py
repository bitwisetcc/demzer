from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from .models import *


def index(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, "core/home.html") # Not implemented yet
    else:    
        return render(request, "core/index.html")


def login(request: HttpRequest):
    return render(request, "core/login.html")


@csrf_exempt  # add auth (not everyone shold be able to see EVERYONE)
@require_POST
def create_user(request: HttpRequest):
    body = json.loads(request.body.decode())

    try:
        if "course" in body:
            user_course = Course.objects.get(slug=body["course"])
        else:
            user_course = None
    except Course.DoesNotExist:
        return Http404(
            "Curso com o campo slug=%s não existe.\nTente os seguintes valores: %s",
            body["course"],
            ", ".join(c.slug for c in Course.objects.all()),
        )
    
    new_user = User(
        name=body["name"],
        email=body["email"],
        password=body["password"],  # check security
        phone=body["phone"],  # validate
        course=user_course,
        gender=body["gender"],  # validate
        birthdate=body["birthdate"],
        user_type=body["user_type"],  # validate
    )
    new_user.save()

    return HttpResponse(":D")


def detail(request: HttpRequest, user_id: int):
    return JsonResponse(User.objects.get(id=user_id).serialize_json())


def all_users(request: HttpRequest):
    everyone = [user.serialize_json() for user in User.objects.all()]

    return JsonResponse({"total": len(everyone), "users": everyone})


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
