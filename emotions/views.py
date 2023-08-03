from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from .models import Emotion
from .serializers import EmotionSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Min
from django.utils import timezone

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role == "내담자"

class EmotionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def is_client_user(self, request):
        try:
            user, _ = JWTAuthentication().authenticate(request)
            return user.role == "내담자"
        except Exception as e:
            return False

    def post(self, request):
        is_client = self.is_client_user(request)
        if not is_client:
            return Response({"detail": "내담자만 감정을 기록할 수 있습니다."}, status=403)

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
            emotion_data['account'] = request.user.id  # 사용자 ID로 변경

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

        # date_joined를 기준으로 감정 기록을 필터링
        emotions = Emotion.objects.filter(account=user, created_at__gte=user.date_joined).order_by('-created_at')

        # totalCount 계산
        first_registration_date = user.date_joined.date()
        today = timezone.now().date()
        total_count = (today - first_registration_date).days

        page = request.query_params.get('page', 1)
        page_size = 7
        start_index = (int(page) - 1) * page_size
        end_index = int(page) * page_size

        emotions_data = []
        for emotion in emotions[start_index:end_index]:
            emotions_data.append({
                'date': emotion.created_at.date().isoformat(),  # 날짜를 ISO 형식으로 변환하여 추가
                'emotions': [
                    {
                        'main_emotion': emotion.main_emotion,
                        'sub_emotion': emotion.sub_emotion,
                        'feeling': str(emotion.feeling),
                        'intensity': emotion.intensity,
                    }
                ],
                'details1': emotion.details1,
                'details2': emotion.details2,
                'details3': emotion.details3,
            })

        response_data = {
            'page': int(page),
            'totalCount': total_count,
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