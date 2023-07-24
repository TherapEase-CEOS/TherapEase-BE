from rest_framework.exceptions import NotFound
from .models import Counselor, User
from .serializer import LoginSerializer, CounselorProfileSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data)



class CounselorProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Counselor.objects.all()
    serializer_class = CounselorProfileSerializer

    def get_object(self):
        user = self.request.user
        counselor, created = Counselor.objects.get_or_create(counselor=user)
        return counselor

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        counselor = self.get_object()

        # 유효한 토큰인지 확인하여 유저 정보를 응답하거나 null 값을 응답
        if request.user.is_authenticated:
            serializer = self.get_serializer(counselor)
            return Response(serializer.data)
        else:
            return Response({'user_info': None}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        counselor = self.get_object()
        serializer = self.get_serializer(counselor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



