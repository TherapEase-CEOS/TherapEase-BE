from datetime import date
from django.db import models

class Schedule(models.Model):
    sunday = models.JSONField(default=list)
    monday = models.JSONField(default=list)
    tuesday = models.JSONField(default=list)
    wednesday = models.JSONField(default=list)
    thursday = models.JSONField(default=list)
    friday = models.JSONField(default=list)
    saturday = models.JSONField(default=list)
    latestUpdated = models.DateField(null=True, blank=True, default=date.today, auto_now=True)

    def __str__(self):
        return f"Schedule - {self.latestUpdated}"

