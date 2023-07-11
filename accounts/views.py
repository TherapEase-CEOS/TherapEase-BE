from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import LoginSerializer

class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data)


