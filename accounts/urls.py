from django.urls import path
from .views import UserLoginView, CounselorProfileView, check_token, LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', CounselorProfileView.as_view(), name='counselor-profile'),
    path('check/', check_token, name='check-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
]