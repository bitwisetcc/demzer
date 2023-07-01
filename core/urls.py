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
]


def school_info(request: HttpRequest):
    return {"school_name": settings.SCHOOL_NAME}
