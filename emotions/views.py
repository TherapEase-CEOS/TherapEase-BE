from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmotionSerializer

class EmotionCreateView(APIView):
    def post(self, request):
        serializer = EmotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '감정이 기록되었습니다.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
