from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from core.models import Member

from management.models import Classroom, Programming, Subject


def chamada(request: HttpRequest):
    return render(request, "grades/chamada.html")


def turmas(request: HttpRequest):
    context = {
        "classrooms": Classroom.objects.all(),
        "subjects": set(
            p.subject.name for p in Programming.objects.filter(teacher=request.user)
        ),
        "students": User.objects.filter(profile__classroom=Classroom.objects.first()),
    }
    return render(request, "grades/turmas.html", context)


def load_students(request: HttpRequest, classroom_pk: int):
    return JsonResponse(
        {
            "students": [
                user.username
                for user in User.objects.filter(profile__classroom=classroom_pk).order_by("username")
            ]
        }
    )
