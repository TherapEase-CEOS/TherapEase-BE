from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Counselee
from .serializers import CounseleeSerializer

class CounseleeCreateView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if code:
            try:
                counselee = Counselee.objects.get(code=code)
                serializer = CounseleeSerializer(counselee)
                return Response(serializer.data)
            except Counselee.DoesNotExist:
                counselee = Counselee(code=code)
                counselee.save()
                serializer = CounseleeSerializer(counselee)
                return Response(serializer.data)
        return Response({'error': 'Code parameter is required.'}, status=400)

class CounseleeListView(APIView):
    def get(self, request):
        counselees = Counselee.objects.all()
        serializer = CounseleeSerializer(counselees, many=True)
        return Response(serializer.data)

class CounseleeUpdateView(APIView):
    def patch(self, request, pk):
        goal = request.data.get('goal')
        try:
            counselee = Counselee.objects.get(pk=pk)
            if goal:
                counselee.goal = goal
                counselee.save()
                serializer = CounseleeSerializer(counselee)
                return Response(serializer.data)
            return Response({'error': '상담목표를 입력해주세요!'}, status=400)
        except Counselee.DoesNotExist:
            return Response({'error': '내담자를 찾을 수 없습니다. 다시 시도해주세요!'}, status=404)

class CounseleeCompleteView(APIView):
    def patch(self, request, pk):
        try:
            counselee = Counselee.objects.get(pk=pk)
            counselee.progress = False
            counselee.save()
            return Response({'message': '상담이 완료되었습니다.'})
        except Counselee.DoesNotExist:
            return Response({'error': '내담자가 존재하지 않습니다.'}, status=404)

class CounseleeDeleteView(APIView):
    def delete(self, request, pk):
        try:
            counselee = Counselee.objects.get(pk=pk)
            counselee.delete()
            return Response({'message': '삭제가 완료되었습니다.'})
        except Counselee.DoesNotExist:
            return Response({'error': '내담자가 존재하지 않습니다.'}, status=404)
