from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmotionSerializer


class EmotionCreateView(APIView):
    def post(self, request):
        try:
            records = request.data.get('records', [])
            for record in records:
                for date, data in record.items():
                    emotions = data.get('emotions', [])
                    details1 = data.get('details1')
                    details2 = data.get('details2')
                    details3 = data.get('details3')
                    for emotion_data in emotions:
                        emotion_data['details'] = {
                            'details1': details1,
                            'details2': details2,
                            'details3': details3
                        }
                        serializer = EmotionSerializer(data=emotion_data)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            return Response({'message': '감정을 기록할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': '감정이 기록되었습니다.'}, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({'message': '올바른 요청 형식이 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)
