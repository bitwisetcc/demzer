from datetime import datetime
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from rolepermissions.checkers import has_role

from core.roles import Teacher
from grades.models import Assessment, Grade, Mention
from management.models import Classroom, Programming, Subject


def chamada(request: HttpRequest):
    subjects = []
    classrooms = []

    for p in Programming.objects.filter(teacher=request.user):
        if p.subject not in subjects:
            subjects.append(p.subject)
            classrooms.append(p.classroom.pk)

    return render(
        request,
        "grades/chamada.html",
        {
            "classrooms": list(
                set([p.classroom for p in request.user.programmings.all()])
            ),
        },
    )


def turmas(request: HttpRequest):
    return render(
        request,
        "grades/turmas.html",
        {
            "classrooms": list(
                set([p.classroom for p in request.user.programmings.all()])
            ),
            "subjects": list(
                set(p.subject for p in Programming.objects.filter(teacher=request.user))
            ),
        },
    )


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


# TODO: block duplicate finals/grades
@require_POST
def post_grade(request: HttpRequest):
    ass = request.POST.get("assessment")
    if ass == "F":
        Mention.objects.create(
            value=request.POST.get("value"),
            student=User.objects.get(pk=request.POST.get("student")),
            teacher=request.user,
            subject=Subject.objects.get(pk=request.POST.get("subject")),
            bimester=request.POST.get("bimester"),
            justification=request.POST.get("justification"),
        )
    else:
        Grade.objects.create(
            assessment=Assessment.objects.get(pk=ass),
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
            "subjects": list(
                set(
                    [
                        str(ass.subject)
                        for ass in Assessment.objects.filter(classroom=classroom_pk)
                    ]
                )
            ),
            "assessments": [
                a.json()
                for a in request.user.assessments.filter(classroom__pk=classroom_pk)
            ],
        }
    )


def load_chamada(request: HttpRequest):
    cls = request.GET.get("classroom")
    teacher = request.GET.get("teacher")
    return JsonResponse(
        {
            "students": [
                {"pk": u.pk, "username": u.username}
                for u in User.objects.filter(profile__classroom__pk=cls).order_by(
                    "username"
                )
            ],
            "programmings": [
                p.json()
                for p in Programming.objects.filter(
                    classroom__pk=cls, teacher__pk=teacher
                )
            ],
        }
    )


def boletim(request: HttpRequest):
    return render(
        request,
        "core/boletim.html",
        {
            "subjects": list(
                set(
                    p.subject for p in request.user.profile.classroom.programmings.all()
                )
            ),
            "mentions": Mention.objects.filter(student=request.user),
        },
    )


def provas(request: HttpRequest, classroom=0):
    if has_role(request.user, Teacher):
        tests = request.user.assessments
        if classroom != 0:
            tests = tests.filter(classroom__pk=classroom)
    else:
        tests = Assessment.objects.filter(classroom=request.user.classroom)
    return render(request, "grades/provas.html", {"tests": tests.all()})
