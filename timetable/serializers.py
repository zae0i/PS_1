# timetable/serializers.py
from rest_framework import serializers
from .models import TimetableEntry

class TimetableEntrySerializer(serializers.ModelSerializer):
    """
    TimetableEntry 직렬화기
    - create(): 로그인 사용자(request.user)를 자동으로 주입
    - validate(): (user, weekday, period) 고유성 검증
    - validate_weekday(): 요일 값 검증 (월~일)
    - validate_period(): 1교시 이상 정수 검증
    """

    class Meta:
        model = TimetableEntry
        # API 계약을 단순하게 유지: user는 서버가 결정하므로 응답/입력에서 제외
        fields = ("id", "weekday", "period", "subject", "teacher")
        read_only_fields = ("id",)

    # 필요 시 허용 요일을 조정하세요.
    _WEEKDAYS = {"월", "화", "수", "목", "금", "토", "일"}

    def validate_weekday(self, value: str) -> str:
        if value not in self._WEEKDAYS:
            raise serializers.ValidationError("요일은 '월','화','수','목','금','토','일' 중 하나여야 합니다.")
        return value

    def validate_period(self, value: int) -> int:
        # 상한(예: 1~12교시)을 두고 싶다면 조건을 추가하세요.
        if value is None or int(value) < 1:
            raise serializers.ValidationError("교시는 1 이상의 정수여야 합니다.")
        return value

    def validate(self, attrs: dict) -> dict:
        """
        (user, weekday, period)의 유일성 보장.
        업데이트 시 자기 자신은 제외합니다.
        """
        request = self.context.get("request")
        user = getattr(request, "user", None)

        # 업데이트의 경우 attrs에 값이 없으면 기존 인스턴스에서 보완
        weekday = attrs.get("weekday", getattr(self.instance, "weekday", None))
        period = attrs.get("period", getattr(self.instance, "period", None))

        if user and weekday and period:
            qs = TimetableEntry.objects.filter(user=user, weekday=weekday, period=period)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("이미 해당 요일/교시에 등록된 항목이 있습니다.")
        return attrs

    def create(self, validated_data: dict) -> TimetableEntry:
        user = self.context["request"].user
        return TimetableEntry.objects.create(user=user, **validated_data)
