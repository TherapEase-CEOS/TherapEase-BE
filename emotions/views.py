from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmotionSerializer


class EmotionCreateView(APIView):
    def post(self, request):
        data = request.data.get('records', [{}])[0]
        emotions_data = data.get('emotions', [])
        details1 = data.get('details1')
        details2 = data.get('details2')
        details3 = data.get('details3')

        # postman test 에서 계속 에러가 났었는데 필수 필드인 main_emotion, sub_emotion, intensity가 제대로 전달되지 않았다는 메세지가 주구장창 뜸.
        # 입력된 데이터에서 해당 필드들을 찾아야한다.
        # 변경 전 코드에서는 details1, details2, details3 필드를 찾고 있었다.
        # 데이터 구조가 일치하지 않아 필드 유효성 검사가 실패했었다.
        # 필수 필드들을 찾아서 데이터에 추가 했다 !
        for emotion_data in emotions_data:
            emotion_data['details1'] = details1
            emotion_data['details2'] = details2
            emotion_data['details3'] = details3

        serializer = EmotionSerializer(data=emotions_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '감정이 기록되었습니다.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 위의 코드에서는 입력된 데이터에서 emotions 필드를 찾아 해당 필드를 emotions_data 변수에 할당한 후, 각각의 emotion_data에 필수 필드들을 추가합니다. 그리고 이 데이터를 시리얼라이저에 전달