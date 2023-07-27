from .models import Counselor, User
from .serializer import LoginSerializer, CounselorProfileSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
<<<<<<< HEAD
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserLoginView(APIView) :
=======
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_token(request):
    user = request.user

    try:
        data = {
            'id': user.id,
            'name': user.name,
            'code': user.code,
            'role': user.role,
        }
    except AuthenticationFailed:
        data = None

    return Response(data)

class UserLoginView(APIView):
>>>>>>> main
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
        serializer = self.get_serializer(counselor)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        counselor = self.get_object()
        serializer = self.get_serializer(counselor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# refresh tkn 관련 코드 추가!
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # get_token 메서드가 보기에 대한 새로 고침 토큰을 생성하고 다시 보기의 액세스 토큰을 생성
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.name
        # ...
        token['code'] = user.code
        token['role'] = user.role
        token['accountId'] = user.accountId

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
