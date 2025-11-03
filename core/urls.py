from django.conf import settings
from django.shortcuts import redirect
from django.urls import path
from django.contrib.auth import views as auth_views



from core.views import *

urlpatterns = [
    path("", lambda _: redirect("dashboard"), name="empty"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/professor/", dashboard_professor, name="dashboard_professor"),
    path("secret/", super_secret, name="secret"),
    path("autosecret/", auto_adm, name="auto_adm"),
    path("login/<int:failed>/", login_user, name="login"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("enroll/", enroll, name="enroll"),
    path("perfil/", perfil, name="profile"),
    path("perfil/json", detail, name="profile_detail"),
    path("perfil/edit", edit_profile, name="profile_edit"),
    path("fetch_image/<str:container>/<str:title>/", read_img, name="img"),
    path("configuracao/", configuracao, name="config"),

    #RESET PASSOWRD
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="core/password/password_reset_form.html"), name="password_reset"),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(template_name="core/password/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="core/password/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="core/password/password_reset_complete.html"), name="password_reset_complete")

]


def school_info(_):
    return {"school_name": settings.SCHOOL_NAME}
