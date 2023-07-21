from rest_framework import serializers

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .models import User, Counselor



class LoginSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        #name = attrs.get('name',None)
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
            'access': str(access),
        }

        return data

class CounselorProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='counselor.name', read_only=True)

    class Meta:
        model = Counselor
        fields = ('name', 'contact', 'introduction')



