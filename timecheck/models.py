from django.db import models
from django.conf import settings  # AUTH_USER_MODEL 참조

class TimeCheck(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    study_time = models.TimeField()

    def __str__(self):
        return f"{self.user.student_id} - {self.date} - {self.study_time}"
