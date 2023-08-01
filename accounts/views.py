from rest_framework_simplejwt.authentication import JWTAuthentication

from counselees import serializers
from .models import Counselor
from .serializer import LoginSerializer, CounselorProfileSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError

@api_view(['GET'])
@authentication_classes([JWTAuthentication])  # JWTAuthentication 사용
@permission_classes([IsAuthenticated])
def check_token(request):
    user = request.user

    try:
        if user.code.startswith('ee'):
            role = 'counselee'
        elif user.code.startswith('or'):
            role = 'counselor'
        else:
            raise serializers.ValidationError("유효하지 않은 코드입니다.")

        data = {
            'id': user.id,
            'name': user.name,
            'code': user.code,
            'role': role,
            'accountId': user.accountId,
        }
    except AuthenticationFailed:
        data = None

    return Response(data)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data)

class IsCounselor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'counselor'

class CounselorProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user

        # 현재 로그인된 사용자의 role이 'counselee'인 경우에는 accountId를 사용하여
        # 해당 accountId를 가진 상담사 프로필을 찾습니다.
        if user.role == 'counselee':
            try:
                counselor = Counselor.objects.get(counselor__accountId=user.accountId)
            except Counselor.DoesNotExist:
                counselor = None
        else:
            # 상담사인 경우 자신의 프로필을 조회합니다.
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

        # 상담사와 내담자를 구분하여 프로필을 반환합니다.
        if counselor and request.user.role == 'counselee':
            serializer = CounselorProfileSerializer(counselor)
            return Response(serializer.data)
        elif counselor and request.user.role == 'counselor':
            serializer = CounselorProfileSerializer(counselor)
            return Response(serializer.data)
        else:
            return Response({'message': '프로필을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        counselor = self.get_object()
        if counselor:
            serializer = CounselorProfileSerializer(counselor, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message': '프로필을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)



class LogoutView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # refresh 토큰을 블랙리스트에 추가하여 무효화합니다.
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
                refresh_token.blacklist()
                return Response(status=status.HTTP_204_NO_CONTENT)  # 성공적으로 로그아웃
            except Exception as e:
                return Response({"error": "로그아웃에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)  # 실패 응답 처리
        else:
            return Response({"error": "로그아웃에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)  # 실패 응답 처리