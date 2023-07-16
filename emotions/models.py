from django.db import models

from accounts.models import User


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
        ('-1', 'Negative'),
        ('0', 'Neutral'),
        ('1', 'Positive'),
    ]

    main_emotion = models.CharField(max_length=10, choices=main_emotion_choices)
    sub_emotion = models.CharField(max_length=50)
    feeling = models.CharField(max_length=2, choices=feeling_choices, default='-1')
    intensity = models.IntegerField()
    details1 = models.TextField(blank=True, null=True)
    details2 = models.TextField(blank=True, null=True)
    details3 = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Using the User model from accounts app
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotions', null=False)

