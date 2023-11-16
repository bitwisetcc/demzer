from django.urls import path
from management.views import *

urlpatterns = [
    path("query/<str:role>/", students, name="query"),
    path("query/<str:role>/<int:coordinator_of>/", students, name="query"),
    path("purge/<str:role>/", purge, name="purge"),
    path("importar/usuários/", import_users, name="import/users"),
    path("cursos/", courses, name="courses"),
    path("cursos/deletar", delete_course, name="delete_course"),
    path("turmas/", classrooms, name="classrooms"),
    path("turmas/deletar", delete_classroom, name="delete_classroom"),
    path("matérias/criar/", create_subject, name="create_subject"),
    path("matérias/importar/", import_subject, name="import_subject"),
    path("horários/<int:classroom_id>/", schedules, name="schedules"),
    path("horários/fix/", delete_schedule, name="fix_schedule"),
]
