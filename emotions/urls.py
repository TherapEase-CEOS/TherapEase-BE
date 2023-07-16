from django.urls import path
from .views import EmotionCreateView, EmotionListView

urlpatterns = [
<<<<<<< HEAD
    path('list/<int:account_id>/', EmotionListView.as_view(), name='emotion-list'),
    path('create/<int:account_id>/', EmotionCreateView.as_view(), name='emotion-create'),
]
=======
    path('', EmotionCreateView.as_view(), name='emotion-create'),
    path('<int:account_id>/', EmotionListView.as_view(), name='emotion-list'),
]
'''
>>>>>>> a8fe3132c09c73fe55f0d001e8205c20a9b81070

