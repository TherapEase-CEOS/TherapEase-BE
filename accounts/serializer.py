from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Counselor

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        access = refresh.access_token

        data['access'] = str(access)
        data['refresh'] = str(refresh)

        return data

class LoginSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        code = attrs.get('code', None)

        try:
            user = User.objects.get(code=code)
        except User.DoesNotExist:
            raise serializers.ValidationError("유효하지 않은 코드입니다.")

        # CustomTokenObtainPairSerializer를 사용하여 토큰 발급
        token_serializer = CustomTokenObtainPairSerializer(data={"username": user.username, "password": code})
        token_serializer.is_valid(raise_exception=True)
        token = token_serializer.validated_data

        data = {
            'id': user.id,
            'name': user.name,
            'code': user.code,
            'role': '내담자' if user.code.startswith('ee') else '상담사',
            'refresh': str(token['refresh']),
            'access': str(token['access']),
        }

        return data

class CounselorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counselor
        fields = ('contact', 'introduction')



