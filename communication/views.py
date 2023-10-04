from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render
from rolepermissions.checkers import has_role, has_permission

from communication.models import Alert, Announcement
from core.utils import upload_img
from management.models import Classroom, Course


def alerts(request: HttpRequest):
    if has_permission(request.user, "see_alerts"):
        return render(
            request,
            "communication/alert/list.html",
            {"alerts": Alert.objects.all()[:20]},
        )

    if request.method == "POST":
        alert = Alert.objects.create(
            emiter=request.user,
            title=request.POST["title"],
            description=request.POST["content"],
            tags=request.POST["tags"],
        )

        try:
            upload_img(request.FILES.get("attachment"), str(alert.pk), "alerts")
        except Exception as exc:
            messages.warning(
                request, "Failed to upload picture: {}".format(exc.args[0])
            )

        messages.success(request, "Alerta criado com sucesso!")

    return render(request, "communication/alert/alert.html")


@login_required
def comunicados(request: HttpRequest):
    if request.method == "POST" and has_role(request.user, "admin"):
        private = "staff_only" not in request.POST
        course = request.POST.get("course")
        classroom = request.POST.get("classroom")

        announcement = Announcement.objects.create(
            title=request.POST.get("title"),
            info=request.POST.get("info"),
            date=datetime.strptime(request.POST["date"], "%Y-%m-%d").date(),
            private=private,
            category=request.POST.get("category"),
            course=Course.objects.get(slug=course) if not private and course else None,
            classroom=Classroom.objects.get(slug=classroom)
            if not private and classroom
            else None,
        )

        try:
            upload_img(
                request.FILES.get("image"), str(announcement.pk), "announcements"
            )
        except Exception as exc:
            messages.warning(
                request, "Failed to upload picture: {}".format(exc.args[0])
            )

        messages.success(
            request, "Comunicado {} criado com sucesso".format(announcement)
        )

    # if has_role(request.user, "student"):
    #     announcements = Announcement.objects.filter(
    #         Q(private=False)
    #         & (
    #             Q(course=None, classroom=None)
    #             | Q(classroom=request.user.profile.classroom)
    #             # | Q(course=request.user.profile.classroom.courses)
    #         )
    #     )
    # else:
    #     announcements = Announcement.objects.all()

    if len(request.GET) == 0:
        announcements = Announcement.objects.all()
    else:
        announcements = Announcement.objects.filter(
            **{k: v for k, v in request.GET.dict().items() if v}
        )

    return render(
        request,
        "communication/announcements.html",
        {"announcements": announcements},
    )
