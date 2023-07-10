from django.urls import path, include
from rest_framework.response import Response

from . import views
from .serializer import LoginSerializer
from .views import UserLoginView
from rest_framework import routers

from rest_framework import viewsets, permissions

class UserLoginViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 로그인 로직 구현
        return Response(serializer.validated_data)

router = routers.DefaultRouter()
router.register(r'user', UserLoginViewSet, basename='user')



urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
]
