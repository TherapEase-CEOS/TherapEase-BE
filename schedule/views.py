from datetime import date, datetime

from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Schedule
from .serializers import ScheduleSerializer
from django.db.models import F

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role == "내담자"

class ScheduleView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def is_client_user(self, request):
        try:
            user, _ = JWTAuthentication().authenticate(request)
            return user.role == "내담자"
        except Exception as e:
            return False

    def get(self, request, pk=None):
        account_id = request.user.accountId # accountId를 받는다

        try:
            schedule = Schedule.objects.get(pk=account_id) # account_id에 해당되는 id의 상담일정표를 받음
            serializer = ScheduleSerializer(schedule)
            response_data = {'data': serializer.data}
            return Response(response_data)
        except Schedule.DoesNotExist: # 없으면 다 false인 상담일정표 반환
            default_schedule_data = {
                "sunday": [False] * 15,
                "monday": [False] * 15,
                "tuesday": [False] * 15,
                "wednesday": [False] * 15,
                "thursday": [False] * 15,
                "friday": [False] * 15,
                "saturday": [False] * 15,
            }
            response_data = {'data': [default_schedule_data]}
            return Response(response_data)

    def put(self, request, pk=None):
        is_client = self.is_client_user(request)
        if is_client: # 내담자이면
            return Response({"detail": "상담사만 상담일정표를 수정할 수 있습니다."}, status=403)
        else : # 상담사이면
            try:
                schedule = Schedule.objects.get(pk=pk)
            except Schedule.DoesNotExist:
                return Response({'message': '시간표를 찾을 수 없습니다.'}, status=404)

            serializer = ScheduleSerializer(schedule, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {'data': serializer.data}
                return Response(response_data)
            else:
                return Response(serializer.errors, status=400)
