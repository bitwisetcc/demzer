from django.db import IntegrityError
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseBadRequest,
    JsonResponse,
    Http404,
)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
import json
import re

from core.models import *
from backend.settings import (
    DEFAULT_COUNTRY,
    DEFAULT_STATE,
    DEFAULT_CITY,
    DEFAULT_BIRTHDATE,
    EMAIL_PATTERN,
)


def doc_to_num(doc: str):
    return int(re.sub(r"[\./-]", "", doc))


@login_required
def index(request: HttpRequest):
    return render(
        request,
        "core/home.html",
        {"users": [user.json() for user in Member.objects.all()]},
    )


def login_user(request: HttpRequest, failed=0):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        user_id = request.POST["user-id"]
        password = request.POST["password"]
        username = User.objects.get(pk=user_id).username

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.add_message(
                request, messages.WARNING, "Senha incorreta. Tente Novamente"
            )
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
    return redirect("home")


# TODO: Create actual emails + prevent email duplication
@login_required
def enroll(request: HttpRequest):
    if not request.user.is_staff or not request.user.is_superuser:
        messages.warning(request, "Apenas administradores podem acessar essa página")
        return redirect("home")

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
                "Algo deu errado tentando registrar o responsável:\n" + err
            )

        return redirect("home")
    else:
        context = {
            "birthdate": DEFAULT_BIRTHDATE,
            "country": DEFAULT_COUNTRY,
            "state": DEFAULT_STATE,
            "city": DEFAULT_CITY,
        }
        return render(request, "core/enroll.html", context)


def courses_editor(request: HttpRequest):
    return render(request, "core/courses.html")

def bulk_enroll(request: HttpRequest):
    return render(request, "core/import_users.html")
    pass

