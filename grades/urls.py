from django.urls import path
from grades.views import *

urlpatterns = [
    path("turmas/", turmas, name="turmas"),
    path("chamada/", chamada, name="chamada"),
    path("getst/<int:classroom_pk>/", load_students, name="alunos"),
    path("new_exercise/", book_exercise, name="new_exercise"),
]
