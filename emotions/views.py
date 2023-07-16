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
        emotions = Emotion.objects.filter(account=user).order_by('-created_at')

        page = request.query_params.get('page', 1)
        page_size = 7
        start_index = (int(page) - 1) * page_size
        end_index = int(page) * page_size

        emotions_data = []
        for emotion in emotions[start_index:end_index]:
            emotions_data.append({
                'main_emotion': emotion.main_emotion,
                'sub_emotion': emotion.sub_emotion,
                'feeling': str(emotion.feeling),
                'intensity': emotion.intensity,
                'details1': emotion.details1,
                'details2': emotion.details2,
                'details3': emotion.details3,
                'account': account_id,
            })

        response_data = {
            'page': int(page),
            'records': emotions_data,
        }
        return Response(response_data)


class EmotionGraphView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_id):
        user = User.objects.get(id=account_id)
        emotions = Emotion.objects.filter(account=user)

        graph_data = []
        for emotion in emotions:
            date = emotion.created_at.date().isoformat()
            emotions_data = {
                'mainEmotion': emotion.main_emotion,
                'subEmotion': emotion.sub_emotion,
                'feeling': emotion.feeling,
                'intensity': emotion.intensity,
            }
            graph_data.append({date: {'emotions': [emotions_data]}})

        response_data = {'records': graph_data}
        return Response(response_data)