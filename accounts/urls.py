from django.urls import path
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserLoginView, CounselorProfileView, check_token

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', CounselorProfileView.as_view(), name='counselor-profile'),
    path('token/',  MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('check/', check_token, name='check-token'),
]

