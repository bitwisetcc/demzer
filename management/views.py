from django.shortcuts import render
from django.http import HttpRequest
import json


def dashboard(request: HttpRequest):
    return render(request, "management/dashboard.html")


def import_students(request: HttpRequest):
    if request.method == "POST":
        print(json.loads(request.body.decode()))
        # User.objects.bulk_create()
        # Member.objects.bulk_create()
    return render(request, "management/students.html")
