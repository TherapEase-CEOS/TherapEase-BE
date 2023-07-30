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
            return Response({'message': '시간표를 찾을 수 없습니다.'}, status=404)

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