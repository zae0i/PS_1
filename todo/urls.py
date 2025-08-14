from django.urls import path
from . import views

urlpatterns = [
    path("", views.todo_list_or_create),              # GET(list by date), POST(create)
    path("<int:todo_id>/", views.update_or_delete_todo),  # PUT, DELETE
]
