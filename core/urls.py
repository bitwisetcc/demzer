from django.conf import settings
from django.urls import path
from core.views import *

urlpatterns = [
    path("", index, name="home"),
    path("login/<int:failed>/", login_user, name="login"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("enroll/", enroll, name="enroll"),
    path("enroll/import/", bulk_enroll, name="import_users"),
    path("courses/", courses_editor, name="courses"),
]


def school_info(request):
    return {"school_name": settings.SCHOOL_NAME}
