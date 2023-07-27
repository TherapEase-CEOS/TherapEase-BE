from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Counselor



class LoginSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
<<<<<<< HEAD
        code = attrs.get('code', None) #pw
        name = attrs.get('name', None) #id
=======
        #name = attrs.get('name',None)
        code = attrs.get('code', None)
>>>>>>> main

        try:
            user = User.objects.get(code=code, name=name)
        except User.DoesNotExist:
            raise serializers.ValidationError("유효하지 않은 코드입니다.")

<<<<<<< HEAD
        # CustomTokenObtainPairSerializer를 사용하여 토큰 발급
        token_serializer = CustomTokenObtainPairSerializer(data={"username": name, "password": code})
        token_serializer.is_valid(raise_exception=True)
        token = token_serializer.validated_data
=======
        if user.code.startswith('ee'):
            role = 'counselee'
        elif user.code.startswith('or'):
            role = 'counselor'
        else:
            raise serializers.ValidationError("유효하지 않은 코드입니다.")

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
>>>>>>> main

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



