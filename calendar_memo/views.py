from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CalendarMemo

def _parse_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def memo_list_or_create(request):
    """
    GET  /api/calendar-memos/?date=2025-08-14  -> 그 날짜 메모 목록
    POST /api/calendar-memos/ {title, content, date: 'YYYY-MM-DD'} -> 생성
    JWT 필요: Authorization: Bearer <access>
    """
    user = request.user

    if request.method == "GET":
        date_str = request.query_params.get("date")
        if not date_str:
            return Response({"message": "날짜 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        date = _parse_date(date_str)
        if not date:
            return Response({"message": "날짜 형식이 올바르지 않습니다. (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)

        memos = CalendarMemo.objects.filter(user=user, date=date).values("id", "title", "content")
        return Response({"memos": list(memos)}, status=status.HTTP_200_OK)

    # POST
    data = request.data or {}
    title = data.get("title")
    content = data.get("content")
    date_str = data.get("date")

    if not all([title, content, date_str]):
        return Response({"message": "제목, 내용, 날짜는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

    date = _parse_date(date_str)
    if not date:
        return Response({"message": "날짜 형식이 올바르지 않습니다. (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)

    CalendarMemo.objects.create(user=user, title=title, content=content, date=date)
    return Response({"message": "메모 저장 완료!"}, status=status.HTTP_201_CREATED)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def memo_update_or_delete(request, memo_id: int):
    """
    PUT    /api/calendar-memos/<id>/ {title?, content?}
    DELETE /api/calendar-memos/<id>/
    JWT 필요: Authorization: Bearer <access>
    """
    try:
        memo = CalendarMemo.objects.get(id=memo_id, user=request.user)
    except CalendarMemo.DoesNotExist:
        return Response({"message": "해당 메모를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        data = request.data or {}
        title = data.get("title")
        content = data.get("content")

        if title is not None:
            memo.title = title
        if content is not None:
            memo.content = content

        memo.save()
        return Response({"message": "메모 수정 완료!"}, status=status.HTTP_200_OK)

    # DELETE
    memo.delete()
    return Response({"message": "메모 삭제 완료!"}, status=status.HTTP_200_OK)
