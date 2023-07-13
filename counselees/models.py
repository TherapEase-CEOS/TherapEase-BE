from django.db import models

class Counselee(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    accountId = models.CharField(max_length=255)
    start = models.DateTimeField()
    progress = models.BooleanField()
    counselingDate = models.CharField(max_length=255)
    goal = models.CharField(max_length=255, default='상담 목표를 입력해주세요!')

    def __str__(self):
        return self.name
