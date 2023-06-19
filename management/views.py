import re

from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render

from core.models import Member


# General queries with auth included
def students(request: HttpRequest, row=1):
    # TODO: check for authorization. If it's an admin, allow everything
    # If it's a teacher, check the classes they're connected to and then get the students
    # Do this here or somewhere else?
    return JsonResponse(
        {
            "users": [
                user.json()
                for user in Member.objects.filter(
                    user__is_staff=False, user__is_superuser=False
                )[40 * (row - 1) : 40 * row]
            ]
        }
    )


def csv_data(line: bytes) -> list[str]:
    return line.decode().replace("\n", "").split(",")


def filter_dict(d: dict, keys: list[str], exclude=False) -> dict:
    return {k: v for k, v in d.items() if (k not in keys if exclude else k in keys)}


# TODO: Select students class? (optionally?)
# TODO: be able to suppress certain errors and leave blank fields
def import_students(request: HttpRequest):
    if request.method == "POST":
        try:
            lines: list[bytes] = list(map(csv_data, request.FILES["users"].readlines()))

            headers: list[str] = lines[0]
            data: list[dict] = []

            # TODO: Validate emails, CPF, RG, gender etc.
            for line in lines[1:]:
                row = dict(zip(headers, line))

                row["phone"] = re.sub(r"[^0-9]+", "", row["phone"])
                row["afro"] = row["afro"] == "true"
                row["cpf"] = re.sub(r"[\./-]", "", row["cpf"])
                row["rg"] = re.sub(r"[\./-]", "", row["rg"])

                data.append(row)

        except IndexError as error:
            return HttpResponseBadRequest("Arquivo vazio. Tente novamente")
        except Exception as error:
            return HttpResponse(f"Erro ao ler arquivo: {error}")

        try:
            users_data = map(
                lambda d: filter_dict(d, ["username", "email", "password"]), data
            )
            users = [User(**user) for user in users_data]
            User.objects.bulk_create(users)
        except Exception as error:
            return HttpResponse(f"Erro ao criar usuários: {error}")

        try:
            # TODO: Optionally reset passwords if they're ancrypted + send reset email
            members_data = map(
                lambda d: filter_dict(d, ["username", "email", "password"], True),
                data,
            )
            print(list(members_data)[0]) # it's not creating the members
            members = [
                Member(**member, user=User.objects.get(username=users[i].username))
                for i, member in members_data
            ]
            Member.objects.bulk_create(members)
            print(Member.objects.first())
        except Exception as error:
            return HttpResponse(f"Erro ao criar perfis: {error}")

        return redirect("dashboard")
    else:
        return render(request, "management/students.html")
