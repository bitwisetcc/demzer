import re
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from rolepermissions.decorators import has_permission_decorator as check_permission
from rolepermissions.decorators import has_role_decorator as check_role
from rolepermissions.roles import assign_role

from backend.settings import (
    DEFAULT_BIRTHDATE,
    DEFAULT_CITY,
    DEFAULT_COUNTRY,
    DEFAULT_STATE,
    EMAIL_PATTERN,
)
from core.models import *


def doc_to_num(doc: str):
    return int(re.sub(r"[\./-]", "", doc))


def login_user(request: HttpRequest, failed=0):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        user_id = request.POST["user-id"]
        password = request.POST["password"]

        try:
            username = User.objects.get(pk=user_id).username
        except User.DoesNotExist:
            messages.warning(request, f"Usuário com RM {user_id} não existe")
            return redirect("login")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.warning(request, "Senha incorreta. Tente Novamente")
            return redirect("login", failed=1)
    else:
        return render(request, "core/login.html", {"no_nav": True, "failed": failed})


@login_required
def logout_user(request: HttpRequest):
    first_name = request.user.username.split()[0]
    logout(request)
    messages.success(
        request,
        f"Você saiu da conta de {first_name}",
    )
    return redirect("dashboard")


# TODO: Create actual emails + prevent email duplication
@check_permission("create_user", redirect_url="dashboard")
def enroll(request: HttpRequest):
    if request.method == "POST":
        username = request.POST["username"].strip()
        first_name = username.split()[0]
        last_name = username.split()[-1]
        birthdate = datetime.strptime(request.POST["birthdate"], "%Y-%m-%d").date()

        try:
            distance = int(request.POST["distance"])
        except ValueError:
            distance = None

        try:
            user = User.objects.create_user(
                username=username,
                email=EMAIL_PATTERN.format(first_name.lower(), last_name.lower()),
                password=first_name + last_name + str(birthdate.year),
            )

            user.save()
        except IntegrityError as err:
            match str(err).split(".")[-1]:
                case "username":
                    messages.add_message(
                        request, messages.ERROR, "Nome de usuário já existe"
                    )
                    return redirect("enroll")
                case "email":
                    raise Http404(
                        f"E-mail já existe"
                    )  # TODO: Add a number to the email

        try:
            profile = Member.objects.create(
                user=user,
                contact_email=request.POST["contact-email"],
                phone=re.sub(r"[^0-9]+", "", request.POST["phone"]),
                birthdate=birthdate,
                gender=request.POST["gender"],
                rg=doc_to_num(request.POST["rg"]),
                cpf=doc_to_num(request.POST["cpf"]),
                public_schooling=request.POST["public-schooling"],
                afro="afro" in request.POST,
                civil_state=request.POST["civil-state"],
                natural_state=request.POST["natural-state"],
                natural_city=request.POST["natural-city"],
                nationality=request.POST["nationality"],
                country_of_origin=request.POST["country-of-origin"],
                cep=request.POST["cep"],
                city=request.POST["residence-city"],
                neighborhood=request.POST["neighborhood"],
                street=request.POST["street"],
                street_number=request.POST["street-number"],
                complement=request.POST["complement"],
                distance=distance,
            )
        except Exception as err:
            return HttpResponseBadRequest(
                "Algo deu errado tentando criar o seu perfil:\n" + err
            )

        try:
            guardian = (
                Relative.objects.create(  # TODO: Check if relative already exists
                    name=request.POST["name-guardian"],
                    email=request.POST["email-guardian"],
                    phone=re.sub(r"[^0-9]+", "", request.POST["phone-guardian"]),
                )
            )

            profile.save()
            profile.relatives.add(guardian)
            profile.save()
        except Exception as err:
            return HttpResponseBadRequest(
                "Algo deu errado ao registrar o responsável:\n" + err
            )

        try:
            assign_role(user, "student")
        except Exception as error:
            # TODO: Doesn't work
            messages.error(request, "Falha ao designar grupo ao usuário: " + str(error))
            return redirect("management/students")

        return redirect("dashboard")
    else:
        context = {
            "birthdate": DEFAULT_BIRTHDATE,
            "country": DEFAULT_COUNTRY,
            "state": DEFAULT_STATE,
            "city": DEFAULT_CITY,
        }
        return render(request, "core/enroll.html", context)


@login_required
def dashboard(request: HttpRequest):
    return render(request, "core/dashboard.html")


def super_secret(request: HttpRequest):
    if request.method == "POST":
        if request.POST["key"] == settings.SECURITY_KEY:
            return HttpResponse("✨")
        else:
            return Http404("booooo")
    return render(request, "core/secret.html", {"no_nav": True})
