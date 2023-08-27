from django.urls import path
from management.views import *

urlpatterns = [
    path("query/<str:role>/<int:row>/", students, name="query"),
    path("purge/<str:role>/", purge, name="purge"),
    path("importar/usuários/", import_users, name="import/users"),
    path("cursos/", courses, name="courses"),
    path("cursos/deletar", delete_course, name="delete_course"),
    path("turmas/", classrooms, name="classrooms"),
    path("turmas/deletar", delete_classroom, name="delete_classroom"),
    path("matérias/criar/", create_subject, name="create_subject"),
    path("matérias/importar/", import_subject, name="import_subject"),
    path("horários/<int:classroom>/", schedules, name="schedules"),
]
