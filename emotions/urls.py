from django.urls import path
from .views import EmotionCreateView, EmotionListView, EmotionGraphView

urlpatterns = [
    path('list/<int:account_id>/', EmotionListView.as_view(), name='emotion-list'),
    path('create/<int:account_id>/', EmotionCreateView.as_view(), name='emotion-create'),
    path('graph/<int:account_id>/', EmotionGraphView.as_view(), name='emotion-graph'),
]

