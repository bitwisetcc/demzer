import re
from datetime import date, datetime

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from django.shortcuts import redirect, render
from rolepermissions.checkers import has_role
from rolepermissions.decorators import has_permission_decorator as check_permission
from rolepermissions.roles import assign_role

from core.models import Member, Relative
from core.roles import Admin
from core.utils import email_address, upload_img
from management.models import Classroom, Programming


@login_required
def dashboard(request: HttpRequest):
    if has_role(request.user, Admin):
        return render(request, "core/dashboard.html")
    else:
        today = date.today()
        weekday = today.weekday()

        date_txt = "{}, {} de {}".format(
            settings.WEEKDAYS[weekday], today.day, settings.MONTHS[today.month]
        )

        programmings = Programming.objects.filter(
            Q(group=None) | Q(group=request.user.profile.division),
            classroom=request.user.profile.classroom,
            day=weekday,
        ).order_by("order")

        

        return render(
            request, "core/home.html", {"programmings": programmings, "day": date_txt}
        )


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
            upload_img(request.FILES.get("picture"), str(user.pk))
        except Exception as exc:
            messages.warning(
                request, "Failed to upload picture: {}".format(exc.args[0])
            )

        try:
            print(1)
            profile = Member.objects.create(
                user=user,
                contact_email=request.POST.get("contact-email"),
                phone=re.sub(r"[^0-9]+", "", request.POST.get("phone")),
                birthdate=birthdate,
                gender=request.POST.get("gender"),
                rg=re.sub(r"[\./-]", "", request.POST.get("rg")),
                cpf=re.sub(r"[\./-]", "", request.POST.get("cpf")),
                afro="afro" in request.POST,
                indigenous="indigenous" in request.POST,
                deficiencies=request.POST.get("deficiencies", None),
                civil_state=request.POST.get("civil-state"),
                cep=request.POST.get("cep"),
                city=request.POST.get("city"),
                neighborhood=request.POST.get("neighborhood"),
                street=request.POST.get("street"),
                street_number=request.POST.get("street-number"),
                complement=request.POST.get("complement"),
            )

            if request.POST.get("role") == "student":
                profile.public_schooling = request.POST.get("public-schooling")
                profile.classroom = Classroom.objects.get(
                    pk=request.POST.get("classroom")
                )

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

        except IntegrityError as error:
            messages.error(request, "Campo de e-mail duplicado: {}".format(error.args[0]))
            return redirect("enroll")

        except Exception as error:
            messages.error(request, "Falha ao criar perfil: {}".format(error.args[0]))
            return redirect("enroll")

        messages.success(request, "Usuário {} criado com sucesso".format(user.pk))
        return redirect("dashboard")
    else:
        context = {
            "birthdate": settings.DEFAULT_BIRTHDATE,
            "country": settings.DEFAULT_COUNTRY,
            "state": settings.DEFAULT_STATE,
            "city": settings.DEFAULT_CITY,
            "classrooms": [
                c
                for c in Classroom.objects.all()
                if date.today().year <= c.year + c.course.duration
            ],
        }
        return render(request, "core/enroll.html", context)


def super_secret(request: HttpRequest):
    if request.method == "POST":
        if request.POST["key"] == settings.SECURITY_KEY:
            username = request.POST["username"].strip()
            first_name = username.split()[0]
            last_name = username.split()[-1]
            birthdate = datetime.strptime(request.POST["birthdate"], "%Y-%m-%d").date()

            try:
                admin = User.objects.create_superuser(
                    username=username,
                    email=settings.EMAIL_PATTERN.format(
                        first_name.lower(), last_name.lower()
                    ),
                    password=request.POST["password"],
                )
            except Exception as error:
                return HttpResponse(
                    "Falha ao cadastrar administrador: {}".format(error.args[0])
                )

            try:
                upload_img(request.FILES.get("picture"), str(admin.pk))
            except Exception as exc:
                messages.warning(
                    request, "Failed to upload picture: {}".format(exc.args[0])
                )

            try:
                Member.objects.create(
                    user=admin,
                    contact_email=request.POST["contact-email"],
                    phone=re.sub(r"[^0-9]+", "", request.POST["phone"]),
                    birthdate=birthdate,
                    gender=request.POST["gender"],
                    rg=re.sub(r"[\./-]", "", request.POST.get("rg")),
                    cpf=re.sub(r"[\./-]", "", request.POST.get("cpf")),
                    afro="afro" in request.POST,
                    indigenous="indigenous" in request.POST,
                    cep=request.POST["cep"],
                    city=request.POST["city"],
                    neighborhood=request.POST["neighborhood"],
                    street=request.POST["street"],
                    street_number=request.POST["street-number"],
                    complement=request.POST["complement"],
                )
            except Exception as error:
                return HttpResponseBadRequest(
                    "Falha ao criar perfil: {}".format(error.args[0])
                )

            try:
                assign_role(admin, Admin)
            except Exception as error:
                raise Http404(
                    "Falha ao designar grupo ao usuário: {}".format(error.args[0])
                )

            messages.success(request, "Usuário {} criado com sucesso".format(admin.pk))

            login(request, admin)
            return redirect("profile")
        else:
            raise Http404("Chave de segurança incorreta")

    context = {
        "birthdate": settings.DEFAULT_BIRTHDATE,
        "country": settings.DEFAULT_COUNTRY,
        "state": settings.DEFAULT_STATE,
        "city": settings.DEFAULT_CITY,
        "no_nav": True,
    }
    return render(request, "core/secret.html", context)


def auto_adm(request: HttpRequest):
    admin = User.objects.create_superuser(
        username="Administrador",
        email=settings.EMAIL_PATTERN.format("adm", "demzer"),
        password="1234",
    )

    Member.objects.create(
        user=admin,
        contact_email="demzer@gmail.com",
        phone=11988887777,
        birthdate=datetime.today().date(),
        gender=Member.Genders.NON_BINARY,
        rg="123456789",
        cpf="12345678901",
        city="São Caetano do Sul",
        neighborhood="Santa Maria",
        street="Taipas",
    )

    assign_role(admin, Admin)
    messages.success(request, "Usuário {} criado com sucesso".format(admin.pk))
    login(request, admin)
    return redirect("profile")


def perfil(request: HttpRequest):
    return render(request, "core/perfil.html")


def read_img(request: HttpRequest, container: str, title: str):
    try:
        service_client = BlobServiceClient(
            settings.STORAGE_BUCKET, DefaultAzureCredential()
        )
        container_client = service_client.get_container_client(container)
        return HttpResponse(container_client.download_blob(title).readall())

    except Exception as exc:
        print("falha ao buscar img de perfil: {}" + exc.args[0])
        raise Http404("Falha ao requisitar imagem")


def configuracao(request: HttpRequest):
    return render(request, "core/configuracao.html")
