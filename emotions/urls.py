from django.urls import path
from .views import EmotionCreateView, EmotionListView

urlpatterns = [
    path('', EmotionCreateView.as_view(), name='emotion-create'),
    path('<int:account_id>/', EmotionListView.as_view(), name='emotion-list'),
]

