from django.urls import path
from .views import *

urlpatterns = [
    path('u/register/', create_user),
    path('u/all/', all_users),
    path('u/students/', all_students),
    path('u/<int:user_id>/', detail),
    path('subjects/new', create_subject),
    path('courses/new', create_course),
    path('classes/new', create_class),
]
