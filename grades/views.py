from datetime import datetime
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from grades.models import Assessment, Grade

from management.models import Classroom, Programming, Subject


def chamada(request: HttpRequest):
    return render(request, "grades/chamada.html")


def turmas(request: HttpRequest):
    context = {
        "classrooms": list(set([p.classroom for p in request.user.programmings.all()])),
        "subjects": list(
            set(p.subject for p in Programming.objects.filter(teacher=request.user))
        ),
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


@require_POST
def post_grade(request: HttpRequest):
    Grade.objects.create(
        assessment=Assessment.objects.get(pk=request.POST.get("assessment")),
        student=User.objects.get(pk=request.POST.get("student")),
        value=request.POST.get("value"),
        justification=request.POST.get("justification"),
    )

    return redirect("turmas")


def load_classroom(request: HttpRequest, classroom_pk: int):
    return JsonResponse(
        {
            "students": [
                {"username": user.username, "pk": user.pk}
                for user in User.objects.filter(
                    profile__classroom=classroom_pk
                ).order_by("username")
            ],
            "assessments": [
                ass.json() for ass in Assessment.objects.filter(classroom=classroom_pk)
            ],
        }
    )


def boletim(request: HttpRequest):
    context = {
        "subjects": list(
            set(p.subject for p in request.user.profile.classroom.programmings.all())
        )
    }

    return render(request, "core/boletim.html", context)
