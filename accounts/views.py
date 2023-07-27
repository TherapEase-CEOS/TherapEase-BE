from rest_framework_simplejwt.authentication import JWTAuthentication

from counselees import serializers
from .models import Counselor
from .serializer import LoginSerializer, CounselorProfileSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.exceptions import AuthenticationFailed


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



