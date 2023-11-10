from django.urls import path
from grades.views import *

urlpatterns = [
    path("turmas/", turmas, name="turmas"),
    path("chamada/", chamada, name="chamada"),
    path("getcls/<int:classroom_pk>/", load_classroom, name="load_class"),
    path("new_exercise/", book_exercise, name="new_exercise"),
    path("boletim/", boletim, name="boletim"),
    path("new/", post_grade, name="post_grade"),
    path("provas/<int:classroom>/", provas, name="provas"),
]
