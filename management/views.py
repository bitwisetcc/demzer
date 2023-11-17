import json
import re
from datetime import datetime as dt
from datetime import timedelta as td

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rolepermissions.checkers import has_role
from rolepermissions.decorators import has_permission_decorator as check_permission
from rolepermissions.roles import assign_role

from core.models import Member
from core.roles import Admin, Teacher
from core.utils import csv_data, dexc, dfilter, get_coordinator
from management.models import Course, Subject, Programming, Classroom


def students(request: HttpRequest, role: str, coordinator_of=None):
    filters = {"groups__name": role, **{k: v for k, v in request.GET.dict().items() if v}}
    print(request.GET.get("profile__birthdate"))

    if coordinator_of is not None and role == "student":
        filters["profile__classroom__in"] = Course.objects.get(
            coordinator__pk=coordinator_of
        ).classrooms.all()

    return JsonResponse(
        {"users": [u.profile.json() for u in User.objects.filter(**filters)]}
    )


@check_permission("delete_user", redirect_url="dashboard")
def purge(request: HttpRequest, role: str):
    User.objects.filter(groups__name=role).delete()
    return redirect("dashboard")


# TODO: be able to suppress certain errors and leave blank fields
def import_users(request: HttpRequest):
    if request.method == "POST":
        try:
            lines: list[str] = list(map(csv_data, request.FILES["users"].readlines()))
            headers: list[str] = lines.pop(0)

            classrooms = {str(c): c for c in Classroom.objects.all()}

            data = [
                {
                    **(row := dict(zip(headers, line))),
                    "phone": re.sub(r"[^0-9]+", "", row["phone"]),
                    "afro": row["afro"] == "true" or row["afro"] == "1",
                    "cpf": re.sub(r"[\./-]", "", row["cpf"]),
                    "rg": re.sub(r"[\./-]", "", row["rg"]),
                    "classroom": classrooms.get(row.get("classroom", ""), None),
                    # TODO: Send reset email
                    "password": make_password(
                        (
                            row["username"].split()[0]
                            + row["username"].split()[-1]
                            + str(dt.strptime(row["birthdate"], "%Y-%m-%d").date().year)
                        )
                        if "reset_password" in request.POST or "password" not in row
                        else row["password"]
                    ),
                }
                for line in lines
            ]

        except IndexError as error:
            messages.error(request, "Arquivo vazio. Tente novamente")
            return redirect("import/users")
        except Exception as error:
            messages.error(request, "Falha ao ler arquivo: {}".format(error))
            return redirect("import/users")

        try:
            users_ghost = User.objects.bulk_create(
                User(**dfilter(user, ["username", "email", "password"]))
                for user in data
            )
            # MySQL doesn't return the pk of the bulk-created rows
            # Rework this if we ever migrate to PosteSQL or MariaDB
            users = User.objects.filter(username__in=[u.username for u in users_ghost])
        except Exception as error:
            messages.error(request, "Falha ao criar usuários: {}".format(error))
            return redirect("import/users")

        try:
            Member.objects.bulk_create(
                Member(**dexc(member, ["username", "email", "password"]), user=user)
                for member, user in zip(data, users)
            )
        except Exception as error:
            messages.error(request, "Falha ao criar perfis: {}".format(error))
            return redirect("import/users")

        try:
            for user in users:
                assign_role(user, request.POST.get("role"))
        except:
            messages.error(request, "Falha ao designar grupos aos usuários")
            return redirect("import/users")

        return redirect("dashboard")
    else:
        return render(request, "management/import.html")


def courses(request: HttpRequest):
    if request.method == "POST":
        pk = request.POST.get("coordinator")

        if request.POST.get("pk") != "0":
            course = Course.objects.get(pk=request.POST.get("pk"))
            course.name = request.POST.get("name")
            course.slug = request.POST.get("slug")
            course.time = request.POST.get("time")
            course.duration = request.POST.get("duration")
            course.info = request.POST.get("info")

            try:
                course.coordinator = get_coordinator(pk)
            except User.DoesNotExist:
                messages.error(request, "Usuário com o ID {} não encontrado".format(pk))
                return redirect("courses")
            except Exception as exc:
                messages.warning(request, exc)
                return redirect("courses")

            course.save()
            messages.success(
                request, "Curso {} editado com sucesso".format(course.slug)
            )
            return redirect("courses")

        try:
            coordinator = get_coordinator(pk)
        except User.DoesNotExist:
            messages.error(request, "Usuário com o ID {} não encontrado".format(pk))
            return redirect("courses")
        except Exception as exc:
            messages.warning(request, exc)
            return redirect("courses")

        course = Course.objects.create(
            name=request.POST.get("name"),
            slug=request.POST.get("slug"),
            time=request.POST.get("time"),
            duration=request.POST.get("duration"),
            info=request.POST.get("info"),
            coordinator=coordinator,
        )

        messages.success(request, "Curso {} criado com sucesso".format(course.slug))
        return redirect("courses")

    if len(request.GET) == 0:
        listing = Course.objects.all()
    else:
        listing = Course.objects.filter(
            **{k: v for k, v in request.GET.dict().items() if v}
        )

    return render(
        request,
        "management/courses.html",
        {
            "courses": listing,
            "subjects": list(Subject.objects.all())[-12:],
        },
    )


@require_POST
@check_permission("create_course")
def delete_course(request: HttpRequest):
    course = Course.objects.get(pk=request.POST.get("pk"))
    course.delete()
    messages.success(request, "Curso {} deletado com sucesso".format(course.slug))
    return redirect("courses")


def classrooms(request: HttpRequest):
    if request.method == "POST":
        course = request.POST.get("course")

        if request.POST.get("pk") != "0":
            classroom = Classroom.objects.get(pk=request.POST.get("pk"))
            classroom.year = request.POST.get("year")

            try:
                classroom.course = Course.objects.get(pk=course)
            except Course.DoesNotExist:
                messages.error(
                    request, "Curso com o ID {} não encontrado".format(course)
                )
                return redirect("classrooms")
            except Exception as exc:
                messages.warning(request, exc)
                return redirect("classrooms")

            classroom.save()
            messages.success(
                request,
                "Turma {} editada com sucesso".format(
                    classroom.course.slug + str(classroom.year)
                ),
            )
            return redirect("classrooms")

        try:
            classroom = Classroom.objects.create(
                course=Course.objects.get(pk=course),
                year=request.POST.get("year"),
            )
        except Course.DoesNotExist:
            messages.error(request, "Curso com o ID {} não encontrado".format(course))
            return redirect("classrooms")
        except Exception as exc:
            messages.warning(request, exc)
            return redirect("classrooms")

        messages.success(
            request,
            "Turma {} criada com sucesso".format(
                classroom.course.slug + str(classroom.year)
            ),
        )
        return redirect("classrooms")

    return render(
        request,
        "management/classrooms.html",
        {
            "classrooms": Classroom.objects.filter(
                **{k: v for k, v in request.GET.dict().items() if v}
            ),
            "courses": Course.objects.all(),
        },
    )


@require_POST
@check_permission("create_classroom")
def delete_classroom(request: HttpRequest):
    classroom = Classroom.objects.get(pk=request.POST.get("pk"))
    classroom.delete()
    messages.success(
        request,
        "Turma {} deletada com sucesso".format(
            classroom.course.slug + str(classroom.year)
        ),
    )
    return redirect("clasrooms")


@require_POST
@check_permission("create_subject")
def import_subject(request: HttpRequest):
    body = json.loads(request.body.decode())
    try:
        Subject.objects.bulk_create(
            Subject(name=name, slug=slug)
            for name, slug in zip(body["names"], body["slugs"])
            if name != "" and slug != ""
        )
        messages.success(request, "Matérias criadas com sucesso.")
        return HttpResponse("Sucesso")
    except Exception as error:
        return HttpResponse("Falha ao criar matérias: {}".format(error))


@require_POST
@check_permission("create_subject")
def create_subject(request: HttpRequest):
    try:
        subj = Subject.objects.create(
            **dfilter(request.POST, ["name", "slug", "description"])
        )
    except Exception as error:
        messages.error(request, "Falha ao criar matéria: {}".format(error))
    finally:
        messages.success(request, "Matéria '{}' criada com sucesso.".format(subj.slug))

    return redirect("courses")


# TODO: if the cell is empty and you try to create a split programming, only the last one is created
def schedules(request: HttpRequest, classroom_id: int):
    if request.method == "POST":
        # TODO: use `has_permission`
        if not has_role(request.user, Admin):
            messages.warning(request, "Você não tem permissão para marcar aulas")
            return redirect("schedules", classroom_id=classroom_id)

        classroom = Classroom.objects.get(pk=classroom_id)

        if "group" in request.POST:
            Programming.create(
                request,
                classroom,
                request.POST["teacher"],
                request.POST["subject"],
                1,
            )
            Programming.create(
                request,
                classroom,
                request.POST["teacher_b"],
                request.POST["subject_b"],
                2,
            )
        else:
            Programming.create(
                request, classroom, request.POST["teacher"], request.POST["subject"]
            )

    if has_role(request.user, Teacher):
        # Teachers
        lessons_qtd = 12
        breaks = [(3, 20), (6, 40), (9, 20)]

        programmings = Programming.objects.filter(teacher=request.user)

        for p in programmings:
            if p.classroom.course.time == Course.Timing.MORNING:
                p.order += 6

        start = dt.strptime(settings.TURNS[Course.Timing.MORNING], "%H:%M")
        classroom = Classroom.objects.first()
        # TODO: mostrar turma, sala? e divisão? nos detalhes
        # TODO: consertar horário pra adaptar entre manhã e tarde
    else:
        # Students and Admins
        lessons_qtd = 6
        breaks = [(3, 20)]

        classroom = request.user.profile.classroom or Classroom.objects.get(
            pk=classroom_id
        )

        start = dt.strptime(settings.TURNS[classroom.course.time], "%H:%M")
        programmings = Programming.objects.filter(classroom=classroom)

    lesson = td(minutes=settings.LESSON_DURATION)
    time_table = [start]
    delay = td(minutes=0)
    for i in range(1, lessons_qtd):
        for b in breaks:
            if i == b[0]:
                delay += td(minutes=b[1])
        time_table.append(start + lesson * i + delay)

    return render(
        request,
        "management/schedules.html",
        {
            "classroom": classroom,
            "time_table": [t.strftime("%H:%M") for t in time_table],
            "subjects": Subject.objects.all(),
            "days": [c for c in Programming.Days.choices],
            "programmings": programmings,
        },
    )


# TODO: check permission
@require_POST
def delete_schedule(request: HttpRequest):
    body = json.loads(request.body.decode())
    classroom_id = int(body["classroom"])

    query = Programming.objects.filter(
        classroom=Classroom.objects.get(pk=classroom_id),
        day=body["day"],
        order=body["time"],
    )

    messages.success(request, "{} aulas foram excluídas".format(query.count()))
    query.delete()
    return redirect("schedules", classroom_id=classroom_id)
