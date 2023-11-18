"""
`urlpatterns` routes URLs to views.
Docs: https://docs.djangoproject.com/en/4.2/topics/http/urls/

Class-based views:
    - Add an import:  from other_app.views import Home
    - Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("management/", include("management.urls")),
    path("grades/", include("grades.urls")),
    path("", include("communication.urls")),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
