from django.urls import path
from .views import (
    CounseleeCreateView,
    CounseleeListView,
    CounseleeUpdateView,
    CounseleeCompleteView,
    CounseleeDeleteView
)
#
urlpatterns = [
    path('', CounseleeCreateView.as_view(), name='counselee-create'),
    path('list/', CounseleeListView.as_view(), name='counselee-list'),
    path('<int:pk>/', CounseleeUpdateView.as_view(), name='counselee-update'),
    path('<int:pk>/', CounseleeCompleteView.as_view(), name='counselee-complete'),
    path('<int:pk>/', CounseleeDeleteView.as_view(), name='counselee-delete'),
]