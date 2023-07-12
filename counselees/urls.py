app_name = "counselees"

from django.urls import path
from accounts.views import UserLoginView, CounselorProfileView

urlpatterns = [
    #path('login/', UserLoginView.as_view(), name='login'), #참고해서 작성하면 될 듯
    #path('profile/<int:id>/', CounselorProfileView.as_view(), name='counselor-profile'),
]
