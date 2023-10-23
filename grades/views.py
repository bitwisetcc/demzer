from django.http import Http404, HttpRequest
from django.shortcuts import render


def chamada(request: Http404):
    return render(request, "grades/chamada.html")


def turmas(request: HttpRequest):
    return render(request, "grades/turmas.html")
