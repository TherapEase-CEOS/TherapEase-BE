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
        if pk is None:
            schedules = Schedule.objects.all()

            # Check if any schedule exists
            if not schedules.exists():
                # If no schedule exists, return default values
                default_schedule_data = {
                    "sunday": [False] * 15,
                    "monday": [False] * 15,
                    "tuesday": [False] * 15,
                    "wednesday": [False] * 15,
                    "thursday": [False] * 15,
                    "friday": [False] * 15,
                    "saturday": [False] * 15,
                }
                return Response({'latestUpdated': None, 'data': {**default_schedule_data}})

            serializer = ScheduleSerializer(schedules, many=True)
            return Response({'data': serializer.data})
        else:
            try:
                schedule = Schedule.objects.get(pk=pk)
                serializer = ScheduleSerializer(schedule)
                return Response({'data': serializer.data})
            except Schedule.DoesNotExist:
                return Response({'message': '시간표를 찾을 수 없습니다.'}, status=404)

    def put(self, request):
        try:
            schedule = Schedule.objects.first()
        except Schedule.DoesNotExist:
            return Response({'message': '시간표를 찾을 수 없습니다.'}, status=404)

        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'latestUpdated': date.today().strftime('%Y-%m-%d'),
                'data': serializer.data
            }
            return Response(response_data)
        else:
            return Response(serializer.errors, status=400)