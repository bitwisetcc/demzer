from datetime import datetime
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from grades.models import Assessment

from management.models import Classroom, Programming, Subject


def chamada(request: HttpRequest):
    return render(request, "grades/chamada.html")


def turmas(request: HttpRequest):
    context = {
        "classrooms": Classroom.objects.all(),
        "subjects": list(
            set(p.subject for p in Programming.objects.filter(teacher=request.user))
        ),
        "students": User.objects.filter(profile__classroom=Classroom.objects.first()),
    }
    return render(request, "grades/turmas.html", context)


@require_POST
def book_exercise(request: HttpRequest):
    Assessment.objects.create(
        subject=Subject.objects.get(pk=request.POST.get("subject")),
        day=datetime.strptime(request.POST.get("until"), "%Y-%m-%d").date(),
        classroom=Classroom.objects.get(pk=request.POST.get("classroom")),
        division=request.POST.get("division") or None,
        bimester=request.POST.get("bimester"),
        kind=request.POST.get("kind"),
        content=request.POST.get("desc"),
    )

    return redirect("turmas")


def load_classroom(request: HttpRequest, classroom_pk: int):
    return JsonResponse(
        {
            "students": [
                user.username
                for user in User.objects.filter(
                    profile__classroom=classroom_pk
                ).order_by("username")
            ],
            "assessments": [
                ass.json()
                for ass in Assessment.objects.filter(classroom=classroom_pk)
            ],
        }
    )
