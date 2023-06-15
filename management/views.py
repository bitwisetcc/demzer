from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.models import User
import json

from core.models import Member


# General queries with auth included
def students(request: HttpRequest, row=1):
    # TODO: check for authorization. If it's an admin, allow everything
    # If it's a teacher, check the classes they're connected to and then get the students
    # Do this here or somewhere else?
    return JsonResponse(
        {
            "users": [
                user.json()
                for user in Member.objects.filter(
                    user__is_staff=False, user__is_superuser=False
                )[40 * (row - 1) : 40 * row]
            ]
        }
    )


# TODO: Select students class? (optionally?)
def import_students(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body.decode()) 
        print(data)
        return HttpResponse(data)
        # User.objects.bulk_create(
        #     [
        #         User(username=data["username"], email=data["email"], password=data["password"])
        #     ]
        # )
        # Member.objects.bulk_create()
    return render(request, "management/students.html")
