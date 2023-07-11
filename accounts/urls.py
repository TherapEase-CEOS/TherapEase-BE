from django.urls import path
from .views import UserLoginView, CounselorProfileView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:id>/', CounselorProfileView.as_view(), name='counselor-profile'),
]
