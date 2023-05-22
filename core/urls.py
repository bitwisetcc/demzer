from django.conf import settings
from django.urls import include, path
from core.views import *

urlpatterns = [
    path("", index, name="home"),
    path("login/<int:failed>/", login_user, name="login"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("enroll/", enroll, name="enroll"),
    path("u/all/", all_users),
    path("u/students/", all_students),
    path("u/<int:user_id>/", detail),
    path("subjects/new/", create_subject),
    path("courses/new/", create_course),
    path("classes/new/", create_class),
]


def school_info(request):
    return {"school_name": settings.SCHOOL_NAME}
