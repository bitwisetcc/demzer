from django.urls import path
from alert.views import *

urlpatterns = [
    path("", new_alert, name="new_alert"),
]
