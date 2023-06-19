from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def new_alert(request: HttpRequest):
    if request.method == "POST":
        return HttpResponse("Falha ao criar denúncia")

    return render(request, "alert/alert.html")
