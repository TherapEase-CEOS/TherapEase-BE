from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Counselor
from .serializer import LoginSerializer, CounselorProfileSerializer

class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data)

class CounselorProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, id):
        try:
            counselor = Counselor.objects.get(counselor_id=id)
        except Counselor.DoesNotExist:
            raise NotFound("상담사 프로필을 수정할 수 없습니다.")

        serializer = CounselorProfileSerializer(counselor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def get(self, request, id):
        try:
            counselor = Counselor.objects.get(counselor_id=id)
        except Counselor.DoesNotExist:
            raise NotFound("상담사 프로필을 찾을 수 없습니다.")

        serializer = CounselorProfileSerializer(counselor)
        return Response(serializer.data)


