from django.urls import path
from management.views import *

urlpatterns = [
    path("query/<str:role>/<int:row>/", students, name="query"),
    path("purge/<str:role>/", purge, name="purge"),
    path("import/users/", import_users, name="import/users"),
    path("courses/", courses, name="courses"),
    path("subjects/new/", create_subject, name="create_subject"),
]
