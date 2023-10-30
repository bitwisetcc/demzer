from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from management.models import Classroom, Programming


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


@require_POST
def book_exercise(request: HttpRequest):
    print(request.POST)
    return HttpResponse("hello")


def load_students(request: HttpRequest, classroom_pk: int):
    return JsonResponse(
        {
            "students": [
                user.username
                for user in User.objects.filter(profile__classroom=classroom_pk).order_by("username")
            ]
        }
    )
