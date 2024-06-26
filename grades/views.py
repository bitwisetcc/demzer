from datetime import datetime
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from rolepermissions.checkers import has_role

from core.roles import Student, Teacher
from core.utils import UTC_date
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
        title=request.POST.get("title"),
        teacher=request.user,
    )

    return redirect("turmas")


@require_POST
def post_grade(request: HttpRequest):
    ass = request.POST.get("assessment")
    if ass == "F":
        print("menção")
        if Mention.objects.filter(
            student__pk=request.POST.get("student"),
            bimester=request.POST.get("bimester"),
            subject__pk=request.POST.get("subject"),
        ).exists():
            messages.error(request, "Essa menção já foi lançada")
        else:
            Mention.objects.create(
                value=request.POST.get("value"),
                student=User.objects.get(pk=request.POST.get("student")),
                teacher=request.user,
                subject=Subject.objects.get(pk=request.POST.get("subject")),
                bimester=request.POST.get("bimester"),
                justification=request.POST.get("justification"),
            )
    else:
        print("nota")
        if Grade.objects.filter(
            student__pk=request.POST.get("student"), assessment__pk=ass
        ).exists():
            messages.error(request, "A nota dessa avaliação já foi lançada")
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
        tests = Assessment.objects.filter(classroom=request.user.profile.classroom)

    start = request.GET.get("start-date")
    end = request.GET.get("end-date")

    filters = {
        "kind": request.GET.get("kind"),
        "classroom__pk": request.GET.get("classroom"),
        "subject__pk": request.GET.get("subject"),
        "day__gte": start and UTC_date(start),
        "day__lte": end and UTC_date(end),
    }

    context = {
        "tests": tests.filter(**{k: v for k, v in filters.items() if v}),
        "cls": classroom,
    }

    if has_role(request.user, Student):
        context["subjects"] = list(
            set(p.subject for p in request.user.profile.classroom.programmings.all())
        )
    elif has_role(request.user, Teacher):
        context["classrooms"] = list(
            set([p.classroom for p in Programming.objects.filter(teacher=request.user)])
        )

    return render(request, "grades/provas.html", context)


@require_POST
def delete_assessment(request: HttpRequest, cls: int):
    ass = Assessment.objects.get(pk=request.POST.get("pk"))
    ass.delete()
    txt = "Prova" if ass.kind == "T" else "Atividade"
    messages.success(request, "{} {} deletada com sucesso".format(txt, ass.title))
    return redirect("provas", cls)
