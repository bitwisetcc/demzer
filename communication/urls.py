from django.urls import path
from communication.views import *

urlpatterns = [
    path("alert/", new_alert, name="new_alert"),
    path("alert/list/", list_alerts, name="list_alerts"),
    path("comunicados/", comunicados, name="comunicados"),
]
