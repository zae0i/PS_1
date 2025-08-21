# calendar_memo/serializers.py
from rest_framework import serializers
from .models import CalendarMemo

class CalendarMemoSerializer(serializers.ModelSerializer):
    # 입력 형식 명시: "YYYY-MM-DD"
    date = serializers.DateField(input_formats=["%Y-%m-%d"])

    class Meta:
        model = CalendarMemo
        # user는 서버에서 주입하므로 제외
        fields = ("id", "date", "title", "content")
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = self.context["request"].user
        return CalendarMemo.objects.create(user=user, **validated_data)
