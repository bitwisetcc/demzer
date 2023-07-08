import os
import re
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from rolepermissions.decorators import has_permission_decorator as check_permission
from rolepermissions.roles import assign_role

from core.models import Member


# General queries with auth included
def students(request: HttpRequest, role: str, row=1):
    # TODO: check for authorization. If it's an admin, allow everything
    # If it's a teacher, check the classes they're connected to and then get the students
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
    return line.decode().replace(os.linesep, "").split(",")


def filter_dict(d: dict, keys: list[str], exclude=False) -> dict:
    return {k: v for k, v in d.items() if (k not in keys if exclude else k in keys)}


# TODO: Select students class? (optionally?)
# TODO: be able to suppress certain errors and leave blank fields
def import_users(request: HttpRequest):
    if request.method == "POST":
        try:
            lines: list[str] = list(map(csv_data, request.FILES["users"].readlines()))
            headers: list[str] = lines.pop(0)

            # TODO: Validate emails, CPF, RG, gender etc.
            data = [
                {
                    **(row := dict(zip(headers, line))),
                    "phone": re.sub(r"[^0-9]+", "", row["phone"]),
                    "afro": row["afro"] == "true" or row["afro"] == "1",
                    "cpf": re.sub(r"[\./-]", "", row["cpf"]),
                    "rg": re.sub(r"[\./-]", "", row["rg"]),
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
                User(**filter_dict(user, ["username", "email", "password"]))
                for user in data
            ]
            User.objects.bulk_create(users)
        except Exception as error:
            return HttpResponse("Falha ao criar usuários: {}".format(error))

        try:
            # TODO: Optionally reset passwords if they're ancrypted + send reset email
            Member.objects.bulk_create(
                Member(
                    **filter_dict(member, ["username", "email", "password"], True),
                    user=users[i],
                )
                for i, member in enumerate(data)
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
