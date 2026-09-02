from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from experiences.views import app_view, manifest_view, service_worker_view


def healthz(request):
    """
    Deploy health check for Render. Deliberately does no database work: it answers
    "did this process start and can it serve a request", which is what a deploy gate
    should test. A check that touched the database would fail the whole deploy over a
    transient connection blip.
    """
    return HttpResponse("ok", content_type="text/plain")


urlpatterns = [
    path("", app_view, name="app"),
    path("healthz", healthz, name="healthz"),
    path("manifest.json", manifest_view, name="manifest"),
    path("sw.js", service_worker_view, name="service-worker"),
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/moods/", include("moods.urls")),
    path("api/buddies/", include("buddies.urls")),
]
