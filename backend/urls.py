"""
`urlpatterns` routes URLs to views.
Docs: https://docs.djangoproject.com/en/4.2/topics/http/urls/

Class-based views:
    - Add an import:  from other_app.views import Home
    - Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("management/", include("management.urls")),
]
