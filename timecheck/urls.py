from django.urls import path
from .views import record_time

urlpatterns = [
    path("", record_time),  # POST /api/timecheck/
]
