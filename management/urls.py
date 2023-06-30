from django.urls import path
from management.views import *

urlpatterns = [
    path("query/students/", students, name="query/students"),
    path("purge/<str:role>", purge, name="purge"),
    path("import/students/", import_students, name="management/students"),
]
