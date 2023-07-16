from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import User

from .models import Emotion
from .serializers import EmotionSerializer

class EmotionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, account_id):
        data = request.data.get('records', [{}])[0]
        date_key = next(iter(data.keys()))  # 첫 번째 키 가져오기
        emotions_data = data.get(date_key, {}).get('emotions', [])
        details1 = data.get(date_key, {}).get('details1')
        details2 = data.get(date_key, {}).get('details2')
        details3 = data.get(date_key, {}).get('details3')

        for emotion_data in emotions_data:
            emotion_data['details1'] = details1
            emotion_data['details2'] = details2
            emotion_data['details3'] = details3
            emotion_data['account'] = account_id

        serializer = EmotionSerializer(data=emotions_data, many=True)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            print(serialized_data)
            return Response({"message": "감정이 기록되었습니다."})
        return Response(serializer.errors, status=400)



class EmotionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_id):
        user = User.objects.get(id=account_id)
        emotions = Emotion.objects.filter(account=user)
        serializer = EmotionSerializer(emotions, many=True)
        return Response(serializer.data)


