from django.urls import path
from .views import EmotionCreateView

urlpatterns = [
    path('emotion/', EmotionCreateView.as_view(), name='emotion-create'),
]
