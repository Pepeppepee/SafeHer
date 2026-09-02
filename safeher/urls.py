from django.contrib import admin
from django.urls import path, include
from experiences.views import app_view, manifest_view, service_worker_view

urlpatterns = [
    path("", app_view, name="app"),
    path("manifest.json", manifest_view, name="manifest"),
    path("sw.js", service_worker_view, name="service-worker"),
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/moods/", include("moods.urls")),
    path("api/buddies/", include("buddies.urls")),
]
