from django.urls import path
from .views import index, history, submit_report, health

urlpatterns = [
    path("", index, name="index"),
    path("history/", history, name="history"),
    path("report/", submit_report, name="report"),
    path("health/", health, name="health"),  # simple healthcheck
]
