from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render
from rolepermissions.checkers import has_role, has_permission

from communication.models import Alert, Announcement, Event
from core.roles import Admin
from core.utils import UTC_date, upload_img
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

    # TODO: targeted announcement for classrooms and courses

    start = request.GET.get("start-date")
    end = request.GET.get("end-date")

    filters = {
        "title__startswith": request.GET.get("title"),
        "date__gt": start and UTC_date(start),
        "date__lt": end and UTC_date(end),
        "category__in": [cat for cat in "rap*" if request.GET.get(cat)],
    }

    announcements = Announcement.objects.filter(
        **{k: v for k, v in filters.items() if v}
    )

    if not has_role(request.user, Admin):
        announcements = announcements.filter(private=False)
        announcements = [a for a in announcements if a.published()]

    return render(
        request,
        "communication/announcements.html",
        {"announcements": announcements},
    )


def events(request: HttpRequest):
    if request.method == "POST" and has_role(request.user, "admin"):
        private = "staff_only" not in request.POST
        course = request.POST.get("course")
        classroom = request.POST.get("classroom")

        event = Event.objects.create(
            title=request.POST.get("title"),
            place=request.POST.get("place"),
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
            upload_img(request.FILES.get("image"), str(event.pk), "events")
        except Exception as exc:
            messages.warning(
                request, "Failed to upload picture: {}".format(exc.args[0])
            )

        messages.success(
            request, "Evento {} criado com sucesso".format(event)
        )

    start = request.GET.get("start-date")
    end = request.GET.get("end-date")

    filters = {
        "title__startswith": request.GET.get("title"),
        "place__startswith": request.GET.get("place"),
        "date__gt": start and UTC_date(start),
        "date__lt": end and UTC_date(end),
    }

    events = Event.objects.filter(
        **{k: v for k, v in filters.items() if v}
    )
    return render(request, "communication/events.html", events)
