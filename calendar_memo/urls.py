from django.urls import path
from . import views

urlpatterns = [
    path('calendar-memos/', views.memo_list_or_create),            # GET, POST
    path('calendar-memos/<int:memo_id>/', views.memo_update_or_delete),  # PUT, DELETE
]
