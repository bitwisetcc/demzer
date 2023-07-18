from django.urls import path
from alert.views import *

urlpatterns = [
    path("", new_alert, name="new_alert"),
    path("list", list_alerts, name="list_alerts"),
]
