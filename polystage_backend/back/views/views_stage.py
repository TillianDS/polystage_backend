from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Stage
from ..serializers import StageSerializer
from rest_framework import status

class StageList(APIView):
    def get (self, request, format = None):
        stage = Stage.objects.all()
        serializer = StageSerializer(stage, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request, format = None):
        serializer = StageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response({"error": "les données ne sont pas valides"}, status=status.HTTP_400_BAD_REQUEST)
    

class StageDetails (APIView):
    def get (self, request, format = None):
        return Response()
    
    def put (self, request, format = None):
        return Response()
    
    def delete(self, request, format = None):
        return Response({"success" : "stage supprimé avec succés"}, status = status.HTTP_200_OK)