from django.urls import path
from .views import ScheduleView

urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule'),
    # path('<int:pk>/', ScheduleView.as_view(), name='schedule-detail'),
]
