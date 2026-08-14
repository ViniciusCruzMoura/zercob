from django.urls import path

from . import views

urlpatterns = [
    path("api/v1/health_check/call", views.health_check, name="health_check"),
]
