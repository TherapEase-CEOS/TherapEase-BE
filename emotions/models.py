from django.db import models


class Emotion(models.Model):
    main_emotion_choices = [
        ('sad', 'Sad'),
        ('scared', 'Scared'),
        ('joyful', 'Joyful'),
        ('powerful', 'Powerful'),
        ('peaceful', 'Peaceful'),
        ('mad', 'Mad'),
    ]

    feeling_choices = [
        (-1, 'Negative'),
        (0, 'Neutral'),
        (1, 'Positive'),
    ]

    main_emotion = models.CharField(max_length=10, choices=main_emotion_choices)
    sub_emotion = models.CharField(max_length=50)
    feeling = models.IntegerField(choices=feeling_choices)
    intensity = models.IntegerField()
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
