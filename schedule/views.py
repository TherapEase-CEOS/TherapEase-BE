from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            schedules = Schedule.objects.all()
            serializer = ScheduleSerializer(schedules, many=True)
            return Response({'data': serializer.data})
        else:
            try:
                schedule = Schedule.objects.get(pk=pk)
                serializer = ScheduleSerializer(schedule)
                return Response(serializer.data)
            except Schedule.DoesNotExist:
                return Response({'message': '시간표를 찾을 수 없습니다.'}, status=404)

    def post(self, request):
        schedule = Schedule.objects.create(
            latestUpdated=None,
            sunday=[None] * 15,
            monday=[None] * 15,
            tuesday=[None] * 15,
            wednesday=[None] * 15,
            thursday=[None] * 15,
            friday=[None] * 15,
            saturday=[None] * 15
        )
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            schedule = Schedule.objects.get(pk=pk)
            serializer = ScheduleSerializer(schedule, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Schedule.DoesNotExist:
            return Response({'message': '시간표를 찾을 수 없습니다.'}, status=404)