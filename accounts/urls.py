from django.urls import path
from . import views

urlpatterns = [
    path("verify-invite/", views.verify_invite),
    path("signup/", views.signup),
    path("login/", views.quick_login),
    path("profile/setup/", views.setup_profile),
    path("profile/", views.my_profile),
]