from django.urls import path
from .views import (
    add_timetable_entry,
    get_timetable,
    update_timetable_entry,
    delete_timetable_entry
)

urlpatterns = [
    path("", get_timetable),                # GET /api/timetable/
    path("add/", add_timetable_entry),       # POST /api/timetable/add/
    path("update/<int:entry_id>/", update_timetable_entry),  # PUT
    path("delete/<int:entry_id>/", delete_timetable_entry),  # DELETE
]
