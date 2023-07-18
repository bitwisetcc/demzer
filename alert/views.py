from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User

from alert.models import Alert


def new_alert(request: HttpRequest):
    if request.method == "POST":
        alert = Alert(
            emiter=request.user,
            title=request.POST["title"],
            description=request.POST["content"],
            tags=request.POST["tags"],
        )

        alert.save()

        return HttpResponse(
            "Emiter: {}<br>Title: {}<br>Description: {}".format(
                alert.emiter, alert.title, alert.description
            )
        )

    return render(request, "alert/alert.html")

def list_alerts(request: HttpRequest):
    return render(request, "alert/list.html", {"alerts": Alert.objects.all()[:20]})
