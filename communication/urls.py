from django.urls import path
from communication.views import *

urlpatterns = [
    path("alerts/", alerts, name="alerts"),
    path("comunicados/", comunicados, name="comunicados"),
]
