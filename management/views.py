from collections import defaultdict
import json
import os
import re
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rolepermissions.decorators import has_permission_decorator as check_permission
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from core.roles import Admin, Student


from core.models import Class, Classroom, Course, Member, Subject


# General queries with auth included
def students(request: HttpRequest, role: str, row=1):
    # TODO: check for authorization. If it's an admin, allow everything
    # If it's a teacher, check the classes they're connected to and then get the students
    # TODO: use Users instead of Members
    return JsonResponse(
        {
            "users": [
                user.json()
                for user in Member.objects.filter(user__groups__name=role)[
                    40 * (row - 1) : 40 * row
                ]
            ]
        }
    )


@check_permission("delete_user", redirect_url="dashboard")
def purge(request: HttpRequest, role: str):
    User.objects.filter(groups__name=role).delete()
    return redirect("dashboard")


def csv_data(line: bytes) -> list[str]:
    return line.decode().replace(os.linesep, "").replace("\n", "").split(",")


def read_csv(request: HttpRequest, file: str) -> tuple[list[list[str]], list[str]]:
    lines = list(map(csv_data, request.FILES[file].readlines()))
    return lines, lines.pop(0)


def dfilter(d: dict, keys: list[str], exclude=False) -> dict:
    return {k: v for k, v in d.items() if (k not in keys if exclude else k in keys)}


# TODO: Select students class? (optionally?)
# TODO: be able to suppress certain errors and leave blank fields
def import_users(request: HttpRequest):
    if request.method == "POST":
        try:
            lines: list[str] = list(map(csv_data, request.FILES["users"].readlines()))
            headers: list[str] = lines.pop(0)

            classrooms = defaultdict(
                None, {c.course.slug + str(c.year): c for c in Classroom.objects.all()}
            )

            data = [
                {
                    **(row := dict(zip(headers, line))),
                    "phone": re.sub(r"[^0-9]+", "", row["phone"]),
                    "afro": row["afro"] == "true" or row["afro"] == "1",
                    "cpf": re.sub(r"[\./-]", "", row["cpf"]),
                    "rg": re.sub(r"[\./-]", "", row["rg"]),
                    "classroom": classrooms.get(row["classroom"]),
                    # TODO: Send reset email
                    "password": make_password(
                        row["username"].split()[0]
                        + row["username"].split()[-1]
                        + str(
                            datetime.strptime(row["birthdate"], "%Y-%m-%d").date().year
                        )
                    )
                    if "reset_password" in request.POST or "password" not in row
                    else row["password"],
                }
                for line in lines
            ]

        except IndexError as error:
            return HttpResponseBadRequest("Arquivo vazio. Tente novamente")
        except Exception as error:
            return HttpResponse("Falha ao ler arquivo: {}".format(error))

        try:
            users = User.objects.bulk_create(
                User(**dfilter(user, ["username", "email", "password"]))
                for user in data
            )
        except Exception as error:
            return HttpResponse("Falha ao criar usuários: {}".format(error))

        try:
            Member.objects.bulk_create(
                Member(
                    **dfilter(member, ["username", "email", "password"], True),
                    user=user,
                )
                for user, member in zip(users, data)
            )
        except Exception as error:
            return HttpResponse("Falha ao criar perfis: {}".format(error))

        try:
            for user in users:
                assign_role(user, request.POST.get("role"))
        except Exception as error:
            messages.error(
                request, "Falha ao designar grupos aos usuários: " + str(error)
            )
            return redirect("import/users")

        return redirect("dashboard")
    else:
        return render(request, "management/import.html")


def get_coordinator(pk: int) -> User:
    coordinator = User.objects.get(pk=int(pk))

    if not has_role(coordinator, ["coordinator", "admin", "teacher"]):
        raise Exception("Usuário {} não tem privilégios necessários".format(pk))

    return coordinator


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
            **({k: v for k, v in request.GET.dict().items() if v})
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
        {"classrooms": Classroom.objects.all(), "courses": Course.objects.all()},
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


def schedules(request: HttpRequest, classroom: int):
    # TODO: implement lunch break
    # TODO: determine class duration (minutes)
    return render(
        request,
        "management/schedules.html",
        {"classroom": Classroom.objects.get(pk=classroom)},
    )
