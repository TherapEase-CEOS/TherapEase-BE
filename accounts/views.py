from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Counselor, User
from .serializer import LoginSerializer, CounselorProfileSerializer
from rest_framework import generics

class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data)

class CounselorProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Counselor.objects.all()
    serializer_class = CounselorProfileSerializer

    def get_object(self):
        user = self.request.user
        try:
            counselor = Counselor.objects.get(counselor=user)
        except Counselor.DoesNotExist:
            raise NotFound("상담사 프로필을 찾을 수 없습니다.")
        return counselor

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


