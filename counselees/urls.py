from django.urls import path
from .views import (
    CounseleeCreateView,
    CounseleeListView,
    CounseleeUpdateView,
    CounseleeCompleteView,
    CounseleeDeleteView
)

urlpatterns = [
    path('create/', CounseleeCreateView.as_view(), name='counselee-create'),
    path('list/', CounseleeListView.as_view(), name='counselee-list'),
    path('update/<int:pk>/', CounseleeUpdateView.as_view(), name='counselee-update'),
    path('complete/<int:pk>/', CounseleeCompleteView.as_view(), name='counselee-complete'),
    path('delete/<int:pk>/', CounseleeDeleteView.as_view(), name='counselee-delete'),
]

