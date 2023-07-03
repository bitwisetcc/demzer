from django.conf import settings
from django.urls import path
from core.views import *

urlpatterns = [
    path("", index, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("login/<int:failed>/", login_user, name="login"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("enroll/", enroll, name="enroll"),
    path("comunicados/", comunicados, name="comunicados"),
    path("perfil/", perfil, name="perfil"),
    path("boletim/", boletim, name="boletim")
]


def school_info(request):
    return {"school_name": settings.SCHOOL_NAME}
