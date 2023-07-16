from rest_framework import serializers
from .models import Emotion


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['main_emotion', 'sub_emotion', 'feeling', 'intensity', 'details1', 'details2', 'details3', 'account']
