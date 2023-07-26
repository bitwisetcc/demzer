import re
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.core.files import File
from django.views.decorators.http import require_POST
from rolepermissions.decorators import has_permission_decorator as check_permission
from rolepermissions.roles import assign_role

from backend.settings import (
    DEFAULT_BIRTHDATE,
    DEFAULT_CITY,
    DEFAULT_COUNTRY,
    DEFAULT_STATE,
    EMAIL_PATTERN,
)
from core.models import *
from core.utils import email_address


def doc_to_num(doc: str):
    return int(re.sub(r"[\./-]", "", doc))


@login_required
def dashboard(request: HttpRequest):
    return render(request, "core/dashboard.html")


def login_user(request: HttpRequest, failed=0):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        user_id = request.POST["user-id"]
        password = request.POST["password"]

        try:
            username = User.objects.get(pk=user_id).username
        except User.DoesNotExist:
            messages.warning(request, "Usuário com RM {} não existe".format(user_id))
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
    messages.success(request, "Você saiu da conta de {}".format(first_name))
    return redirect("dashboard")


# TODO: Create actual emails
@check_permission("create_user", redirect_url="dashboard")
def enroll(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        first_name = username.split()[0]
        last_name = username.split()[-1]
        birthdate = datetime.strptime(request.POST["birthdate"], "%Y-%m-%d").date()
        picture = File(request.FILES.get("picture"))

        try:
            user = User.objects.create_user(
                username=username,
                email=email_address(username),
                password=first_name + last_name + str(birthdate.year),
            )

        except IntegrityError:
            messages.error(request, "Nome de usuário já existe")
            return redirect("enroll")

        try:
            profile = Member.objects.create(
                user=user,
                contact_email=request.POST.get("contact-email"),
                phone=re.sub(r"[^0-9]+", "", request.POST.get("phone")),
                birthdate=birthdate,
                gender=request.POST.get("gender"),
                rg=doc_to_num(request.POST.get("rg")),
                cpf=doc_to_num(request.POST.get("cpf")),
                afro="afro" in request.POST,
                civil_state=request.POST.get("civil-state"),
                cep=request.POST.get("cep"),
                city=request.POST.get("residence-city"),
                neighborhood=request.POST.get("neighborhood"),
                street=request.POST.get("street"),
                street_number=request.POST.get("street-number"),
                complement=request.POST.get("complement"),
                picture=picture if picture.readable() else None,
            )

            if request.POST.get("role") == "student":
                profile.public_schooling = request.POST.get("public-schooling")
                profile.natural_state = request.POST.get("natural-state")
                profile.natural_city = request.POST.get("natural-city")
                profile.nationality = request.POST.get("nationality")
                profile.country_of_origin = request.POST.get("country-of-origin")

                try:
                    guardian, created = Relative.objects.get_or_create(
                        name=request.POST.get("name-guardian"),
                        email=request.POST.get("email-guardian"),
                        phone=re.sub(
                            r"[^0-9]+", "", request.POST.get("phone-guardian")
                        ),
                    )

                    profile.save()
                    profile.relatives.add(guardian)

                    if not created:
                        messages.info(
                            request, "Responsável já encontrado. Verifique o perfil"
                        )

                except Exception as error:
                    messages.warning(request, "Falha ao associar responsável")

            profile.save()

            try:
                assign_role(user, request.POST.get("role"))
            except Exception as error:
                messages.warning(request, "Falha ao designar grupo ao usuário")

        except Exception as error:
            return HttpResponseBadRequest(
                "Falha ao criar perfil: {}".format(error.args[0])
            )

        messages.success(request, "Usuário {} criado com sucesso".format(user.pk))
        return redirect("dashboard")
    else:
        context = {
            "birthdate": DEFAULT_BIRTHDATE,
            "country": DEFAULT_COUNTRY,
            "state": DEFAULT_STATE,
            "city": DEFAULT_CITY,
        }
        return render(request, "core/enroll.html", context)


def super_secret(request: HttpRequest):
    if request.method == "POST":
        if request.POST["key"] == settings.SECURITY_KEY:
            username = request.POST["username"].strip()
            first_name = username.split()[0]
            last_name = username.split()[-1]
            birthdate = datetime.strptime(request.POST["birthdate"], "%Y-%m-%d").date()
            picture = File(request.FILES.get("picture"))

            try:
                admin = User.objects.create_superuser(
                    username=username,
                    email=EMAIL_PATTERN.format(first_name.lower(), last_name.lower()),
                    password=request.POST["password"],
                )

                admin.save()
            except Exception as error:
                return HttpResponse(
                    "Falha ao cadastrar administrador: {}".format(error.args[0])
                )

            try:
                profile = Member.objects.create(
                    user=admin,
                    contact_email=request.POST["contact-email"],
                    phone=re.sub(r"[^0-9]+", "", request.POST["phone"]),
                    birthdate=birthdate,
                    gender=request.POST["gender"],
                    rg=doc_to_num(request.POST["rg"]),
                    cpf=doc_to_num(request.POST["cpf"]),
                    afro="afro" in request.POST,
                    cep=request.POST["cep"],
                    city=request.POST["residence-city"],
                    neighborhood=request.POST["neighborhood"],
                    street=request.POST["street"],
                    street_number=request.POST["street-number"],
                    complement=request.POST["complement"],
                    picture=picture if picture.readable() else None,
                )
                profile.save()
            except Exception as error:
                return HttpResponseBadRequest(
                    "Falha ao criar perfil: {}".format(error.args[0])
                )

            try:
                assign_role(admin, "admin")
            except Exception as error:
                return Http404(
                    "Falha ao designar grupo ao usuário: {}".format(error.args[0])
                )

            messages.success(request, "Usuário {} criado com sucesso".format(admin.pk))
            return redirect("login")
        else:
            return Http404("Chave de segurança incorreta")

    context = {
        "birthdate": DEFAULT_BIRTHDATE,
        "country": DEFAULT_COUNTRY,
        "state": DEFAULT_STATE,
        "city": DEFAULT_CITY,
        "no_nav": True,
    }
    return render(request, "core/secret.html", context)


def comunicados(request: HttpRequest):
    return render(request, "core/comunicados.html")


def perfil(request: HttpRequest):
    return render(request, "core/perfil.html")


def boletim(request: HttpRequest):
    return render(request, "core/boletim.html")


def obs_aluno(request):
    obs = request.POST.get("obs")
    return obs


def profile_picture(request: HttpRequest):
    if request.method == "POST":
        pic = File(request.FILES.get("picture"))
        if not pic.readable():
            return HttpResponseBadRequest("Arquivo vazio ou corrompido")

        member = Member.objects.get(user=request.user)
        member.picture = pic
        member.save()

        return redirect("perfil")

    return HttpResponse(request.user.profile.picture.url)
