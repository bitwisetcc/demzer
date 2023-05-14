from django.http import HttpResponse, HttpRequest, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from backend.settings import (
    DEFAULT_CITY,
    DEFAULT_STATE,
    DEFAULT_STUDENT_BIRTHDATE,
)
import json

from core.forms import StudentEnrollmentForm
from core.models import *


def index(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, "core/home.html")  # Not implemented yet
    else:
        return render(request, "core/home.html")


def login(request: HttpRequest):
    return render(request, "core/login.html")


def register(request: HttpRequest):
    form = StudentEnrollmentForm()
    return render(request, "core/form.html", { "form": form.render() })


def enroll(request: HttpRequest):
    if request.method == "POST":
        try:
            for key in request.POST.keys():
                print(key)
            return HttpResponse("haiii")            
        except: pass
    else:
        context = {"city": DEFAULT_CITY, "state": DEFAULT_STATE, "birthdate": DEFAULT_STUDENT_BIRTHDATE}
        return render(request, "core/enroll.html", context)


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
