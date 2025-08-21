# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def health(_):
    return JsonResponse({"ok": True, "app": "PS_1"})

urlpatterns = [
    path("admin/", admin.site.urls),

    # 헬스체크
    path("api/health/", health),

    # JWT/계정
    path("api/accounts/", include("accounts.urls")),

    # 앱별 API
    path("api/timecheck/", include("timecheck.urls")),
    path("api/timetable/", include("timetable.urls")),
    path("api/todo/", include("todo.urls")),
    path("api/memo/", include("calendar_memo.urls")),

    # OpenAPI 스키마 & Swagger UI (drf-spectacular + sidecar 정적 자산)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
