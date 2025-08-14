from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT/계정 (accounts.urls에 signup, jwt/login/refresh/verify, me 포함)
    path("api/accounts/", include("accounts.urls")),

    # 앱별 API
    path("api/timecheck/", include("timecheck.urls")),
    path("api/timetable/", include("timetable.urls")),
    path("api/todo/", include("todo.urls")),
    path("api/memo/", include("calendar_memo.urls")),
]
