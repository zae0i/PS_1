# timecheck/serializers.py
from rest_framework import serializers
from .models import TimeCheck

class TimeCheckSerializer(serializers.ModelSerializer):
    # 입력 포맷을 명시(예: "2025-06-26", "01:30:00")
    date = serializers.DateField(input_formats=["%Y-%m-%d"])
    study_time = serializers.TimeField(input_formats=["%H:%M:%S"])

    class Meta:
        model = TimeCheck
        # user는 서버에서 주입하므로 제외
        fields = ("id", "date", "study_time")
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = self.context["request"].user
        return TimeCheck.objects.create(user=user, **validated_data)
