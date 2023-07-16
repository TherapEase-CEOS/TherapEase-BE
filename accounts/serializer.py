from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer

from .models import User, Counselor

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Access 토큰 유효 기간 설정
        token.set_exp(lifetime=timedelta(days=7))  # 7일로 설정

        return token

    def validate(self, attrs):
        code = attrs.get('code', None)

        try:
            user = User.objects.get(code=code)
        except User.DoesNotExist:
            raise serializers.ValidationError("유효하지 않은 코드입니다.")

        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Access 토큰 유효 기간 설정
        access_token = self.get_token(self.user)
        access_token.set_exp(lifetime=timedelta(days=7))  # 7일로 설정 (원하는 유효 기간으로 변경 가능)

        # 만료 시간이 남아있는 경우에만 Refresh 토큰을 사용하여 자동 재발급
        refresh_token = data['refresh']
        refresh_token_exp = refresh_token.get('exp')
        current_time = timezone.now().timestamp()
        if refresh_token_exp and refresh_token_exp > current_time:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token
            data['access'] = str(new_access_token)

        return data

class CounselorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counselor
        fields = ('contact', 'introduction')

class LoginSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        code = attrs.get('code', None)

        try:
            user = User.objects.get(code=code)
        except User.DoesNotExist:
            raise serializers.ValidationError("유효하지 않은 코드입니다.")

        if user.code.startswith('ee'):
            role = '내담자'
        elif user.code.startswith('or'):
            role = '상담사'
        else:
            raise serializers.ValidationError("유효하지 않은 코드입니다.")

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        data = {
            'id': user.id,
            'name': user.name,
            'code': user.code,
            'role': role,
            'refresh': str(refresh),
            'access': str(access)
        }

        return data
