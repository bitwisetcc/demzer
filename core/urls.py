from django.conf import settings
from django.shortcuts import redirect
from django.urls import path

from core.views import *

urlpatterns = [
    path("", lambda _: redirect("dashboard"), name="empty"),
    path("dashboard/", dashboard, name="dashboard"),
    path("secret/", super_secret, name="secret"),
    path("login/<int:failed>/", login_user, name="login"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("enroll/", enroll, name="enroll"),
    path("comunicados/", comunicados, name="comunicados"),
    path("perfil/", perfil, name="perfil"),
    path("boletim/", boletim, name="boletim"),
    path("eventos/", eventos, name="eventos"),
]


def school_info(_):
    return {"school_name": settings.SCHOOL_NAME}
