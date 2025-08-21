# calendar_memo/views.py
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CalendarMemo
from .serializers import CalendarMemoSerializer  # ★ 추가

def _parse_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def memo_list_or_create(request):
    user = request.user

    if request.method == "GET":
        date_str = request.query_params.get("date")
        if not date_str:
            return Response({"message": "날짜 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        date = _parse_date(date_str)
        if not date:
            return Response({"message": "날짜 형식이 올바르지 않습니다. (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)

        qs = CalendarMemo.objects.filter(user=user, date=date).order_by("id")
        ser = CalendarMemoSerializer(qs, many=True)
        return Response({"memos": ser.data}, status=status.HTTP_200_OK)

    # POST
    ser = CalendarMemoSerializer(data=request.data, context={"request": request})
    ser.is_valid(raise_exception=True)
    obj = ser.save()
    return Response({"message": "메모 저장 완료!", "item": CalendarMemoSerializer(obj).data},
                    status=status.HTTP_201_CREATED)

@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def memo_update_or_delete(request, memo_id: int):
    try:
        memo = CalendarMemo.objects.get(id=memo_id, user=request.user)
    except CalendarMemo.DoesNotExist:
        return Response({"message": "해당 메모를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        ser = CalendarMemoSerializer(memo, data=request.data, partial=True, context={"request": request})
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response({"message": "메모 수정 완료!", "item": CalendarMemoSerializer(obj).data},
                        status=status.HTTP_200_OK)

    memo.delete()
    return Response({"message": "메모 삭제 완료!"}, status=status.HTTP_200_OK)
