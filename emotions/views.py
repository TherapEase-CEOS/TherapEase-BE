from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmotionSerializer


class EmotionCreateView(APIView):
    def post(self, request):
        data = request.data.get('records', [{}])
        emotions_data = []
        for record in data:
            for date, record_data in record.items():
                emotions_data.extend(record_data.get('emotions', []))
                details1 = record_data.get('details1')
                details2 = record_data.get('details2')
                details3 = record_data.get('details3')
                print(data)

                # 필수 필드들을 찾아서 데이터에 추가
                for emotion_data in emotions_data:
                    emotion_data['details1'] = details1
                    emotion_data['details2'] = details2
                    emotion_data['details3'] = details3

        serializer = EmotionSerializer(data=emotions_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '감정이 기록되었습니다.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
