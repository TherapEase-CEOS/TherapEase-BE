from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Schedule
from .serializers import ScheduleSerializer
from rest_framework import status

class ScheduleView(APIView):
    def get(self, request):
        try:
            schedule = Schedule.objects.latest('latestUpdated')
            serializer = ScheduleSerializer(schedule)
            return Response(serializer.data)
        except Schedule.DoesNotExist:
            return Response({"message": "시간표를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        try:
            schedule = Schedule.objects.latest('latestUpdated')
            schedule_serializer = ScheduleSerializer(schedule, data=request.data, partial=True)
            if schedule_serializer.is_valid():
                schedule_serializer.save()
                return Response(schedule_serializer.data)
            return Response(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Schedule.DoesNotExist:
            return Response({"message": "상담 일정표를 수정할 수 없습니다."}, status=status.HTTP_504_GATEWAY_TIMEOUT)

