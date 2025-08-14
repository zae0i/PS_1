from django.db import models
from django.conf import settings

class TimetableEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=10)  # 예: '월', '화', '수', ...
    period = models.IntegerField()             # 예: 1, 2, 3교시
    subject = models.CharField(max_length=50)  # 과목명 직접입력
    teacher = models.CharField(max_length=50)  # 교사명 직접입력

    class Meta:
        unique_together = ('user', 'weekday', 'period')  # 사용자별 중복 방지

    def __str__(self):
        return f"{self.user.student_id} - {self.weekday}{self.period}교시"
