from django.urls import path
from . import views

urlpatterns = [
    path("intent/", views.create_intent),
    path("threads/", views.my_threads),
    path("threads/<uuid:thread_id>/", views.thread_detail),
    path("threads/<uuid:thread_id>/messages/", views.send_message),
    path("threads/<uuid:thread_id>/report/", views.report_user),
]
