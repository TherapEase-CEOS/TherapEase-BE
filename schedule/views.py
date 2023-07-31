from datetime import date, datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Schedule
from .serializers import ScheduleSerializer
from django.db.models import F

# 시간 반환형식 변경
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

class ScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            schedules = Schedule.objects.all()

            # 시간표가 없을 때 기본 값을 반환합니다.
            if not schedules.exists():
                default_schedule_data = {
                    "sunday": [False] * 15,
                    "monday": [False] * 15,
                    "tuesday": [False] * 15,
                    "wednesday": [False] * 15,
                    "thursday": [False] * 15,
                    "friday": [False] * 15,
                    "saturday": [False] * 15,
                }
                response_data = {'data': [{'latestUpdated': formatted_datetime, **default_schedule_data}]}
                return Response(response_data)

            serializer = ScheduleSerializer(schedules, many=True)
            response_data = {'data': serializer.data}
            return Response(response_data)
        else:
            try:
                schedule = Schedule.objects.get(pk=pk)
                serializer = ScheduleSerializer(schedule)
                response_data = {'data': [serializer.data]}
                return Response(response_data)
            except Schedule.DoesNotExist:
                return Response({'message': '시간표를 찾을 수 없습니다.'}, status=404)

    def put(self, request, pk=None):
        try:
            schedule = Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            return Response({'message': '시간표를 찾을 수 없습니다.'}, status=404)

        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {'data': [serializer.data]}
            return Response(response_data)
        else:
            return Response(serializer.errors, status=400)
