from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'code')

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
