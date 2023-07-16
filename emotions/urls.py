'''
from django.urls import path
from .views import EmotionCreateView, EmotionListView

urlpatterns = [
    path('', EmotionCreateView.as_view(), name='emotion-create'),
    path('<int:account_id>/', EmotionListView.as_view(), name='emotion-list'),
]
'''

from django.urls import path
from .views import create_emotion, list_emotions, graph_emotions

app_name = 'emotions'

urlpatterns = [
    path('create/<int:pk>/', create_emotion, name='create'),
    path('list/<int:pk>/', list_emotions, name='list'),
    path('graph/<int:pk>/', graph_emotions, name='graph'),
]

