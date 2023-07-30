from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Schedule
from .serializers import ScheduleSerializer
from django.db.models import F


class ScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        role = user.role
        accountId = user.accountId

        try:
            if role == '상담사':
                # 상담사인 경우, 자신의 스케줄을 반환합니다.
                schedule = Schedule.objects.get(accountId=accountId)
            else:
                # 내담자인 경우, 연결된 상담사의 스케줄을 반환합니다.
                counselor_schedule = Schedule.objects.get(accountId=accountId)
                serializer = ScheduleSerializer(counselor_schedule)
                return Response({'data': serializer.data})

        except Schedule.DoesNotExist:
            # 기본 스케줄 데이터 생성
            default_schedule_data = {
                "sunday": [False] * 15,
                "monday": [False] * 15,
                "tuesday": [False] * 15,
                "wednesday": [False] * 15,
                "thursday": [False] * 15,
                "friday": [False] * 15,
                "saturday": [False] * 15,
            }
            # 데이터가 없는 경우 기본 스케줄 데이터를 반환합니다.
            return Response({'latestUpdated': None, 'data': {**default_schedule_data}})

        serializer = ScheduleSerializer(schedule)
        return Response({'data': serializer.data})

    def put(self, request):
        try:
            schedule = Schedule.objects.first()
        except Schedule.DoesNotExist:
            return Response({'message': '시간표를 찾을 수 없습니다.'}, status=404)

        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():

            response_data = {
                'latestUpdated': date.today().strftime('%Y-%m-%d'),
                'data': serializer.data
            }
            return Response(response_data)
        else:
            return Response(serializer.errors, status=400)