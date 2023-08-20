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
from core.roles import Admin


from core.models import Class, Course, Member, Subject


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

            data = [
                {
                    **(row := dict(zip(headers, line))),
                    "phone": re.sub(r"[^0-9]+", "", row["phone"]),
                    "afro": row["afro"] == "true" or row["afro"] == "1",
                    "cpf": re.sub(r"[\./-]", "", row["cpf"]),
                    "rg": re.sub(r"[\./-]", "", row["rg"]),
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
            users = [
                User(**dfilter(user, ["username", "email", "password"]))
                for user in data
            ]
            User.objects.bulk_create(users)
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
            messages.success(request, "Curso {} editado com sucesso".format(course.slug))
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

    return render(
        request,
        "management/courses.html",
        {
            "courses": Course.objects.all(),
            "subjects": list(Subject.objects.all())[-12:],
        },
    )


@require_POST
@check_permission("create_subject")
def create_subject(request: HttpRequest):
    if "import" in request.POST:
        lines, headers = read_csv(request, "import_file")
        data = [dict(zip(headers, l)) for l in lines]

        try:
            Subject.objects.bulk_create(
                Subject(name=subj["name"], slug=subj["slug"]) for subj in data
            )
        except IndexError as error:
            return HttpResponseBadRequest("Arquivo vazio. Tente novamente")
        except Exception as error:
            return HttpResponse("Falha ao ler arquivo: {}".format(error))

    else:
        try:
            subj = Subject.objects.create(
                **dfilter(request.POST, ["name", "slug", "description"])
            )
        except Exception as error:
            messages.error(request, "Falha ao criar matéria: {}".format(error))
        finally:
            messages.success(
                request, "Matéria '{}' criada com sucesso.".format(subj.slug)
            )

    return redirect("courses")
