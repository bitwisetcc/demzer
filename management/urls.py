from django.urls import path
from management.views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("import/students/", import_students, name="management/students"),
    path("query/students/", students, name="query/students"),
]
