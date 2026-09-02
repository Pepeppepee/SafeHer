from django.urls import path
from . import views

urlpatterns = [
    path("find/", views.find_match),
    path("respond/", views.respond_to_match),
    path("checkin/<uuid:response_id>/", views.check_in),
    path("pending/", views.pending_checkins),
]
