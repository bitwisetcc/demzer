from django.urls import path
from grades.views import *

urlpatterns = [
    path("turmas/", turmas, name="turmas"),
    path("chamada/", chamada, name="chamada"),
]
