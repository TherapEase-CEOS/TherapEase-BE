from rest_framework import serializers
from .models import Counselee

class CounseleeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counselee
        fields = '__all__'
