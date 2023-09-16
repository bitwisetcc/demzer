from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render
from rolepermissions.checkers import has_role

from communication.models import Alert, Announcement
from management.models import Classroom, Course


def new_alert(request: HttpRequest):
    if request.method == "POST":
        alert = Alert.objects.create(
            emiter=request.user,
            title=request.POST["title"],
            description=request.POST["content"],
            tags=request.POST["tags"],
        )

        messages.success(request, "Alerta criado com sucesso!")

    return render(request, "alert/alert.html")


def list_alerts(request: HttpRequest):
    return render(request, "alert/list.html", {"alerts": Alert.objects.all()[:20]})


@login_required
def comunicados(request: HttpRequest):
    if request.method == "POST" and has_role(request.user, "admin"):
        picture = File(request.FILES.get("image"))
        private = "staff_only" not in request.POST
        course = request.POST.get("course")
        classroom = request.POST.get("classroom")

        

        pk = Announcement.objects.create(
            title=request.POST.get("title"),
            info=request.POST.get("info"),
            image=picture if picture.readable() else None,
            private=private,
            course=Course.objects.get(slug=course) if not private and course else None,
            classroom=Classroom.objects.get(slug=classroom)
            if not private and classroom
            else None,
        )

        messages.success(request, "Comunicado {} criado com sucesso".format(pk))

    if has_role(request.user, "student"):
        announcements = Announcement.objects.filter(
            Q(private=False)
            & (
                Q(course=None, classroom=None)
                | Q(classroom=request.user.profile.classroom)
                # | Q(course=request.user.profile.classroom.courses)
            )
        )
    else:
        announcements = Announcement.objects.all()

    return render(
        request, "core/comunicados.html", {"announcements": Announcement.objects.all()}
    )
