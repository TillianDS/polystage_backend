from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Stage, Tuteur
from ..serializers import StageSerializer, StageTuteurSerializer
from rest_framework import status
from polystage_backend.permissions import *

class StageList(APIView):
    """
    permet d'obtenir la liste des stages ou de créer un stage 
    """
    def getDate(self, request, date_str):
        date = datetime.strptime(date_str, '%d-%m-%Y').date()
        return date
    
    def get (self, request, format = None):
        stage = Stage.objects.all()
        serializer = StageSerializer(stage, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request, format = None):
        date_fin = self.getDate(request, request.data['date_fin'])
        date_debut = self.getDate(request, request.data['date_debut'])

        data = request.data.copy()
        data['date_debut'] = date_debut
        data['date_fin'] = date_fin
        
        serializer = StageSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StageDetails (APIView):
    def getDate(self, request, date_str):
        date = datetime.strptime(date_str, '%d-%m-%Y').date()
        return date
    
    def get (self, request, pk, format = None):
        stage = Stage.objects.get(pk = pk)
        serializer = StageSerializer(stage)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put (self, request, pk, format = None):
        date_fin = self.getDate(request, request.data['date_fin'])
        date_debut = self.getDate(request, request.data['date_debut'])

        data = request.data.copy()
        data['date_debut'] = date_debut
        data['date_fin'] = date_fin

        stage = Stage.objects.get(pk = pk)
        serializer = StageSerializer(stage, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        stage = Stage.objects.get(pk=pk)
        stage.delete()
        return Response({"success" : "stage supprimé avec succés"}, status = status.HTTP_200_OK)

"""
retourne les stages et leur étudiants, soutenance, session suivis par tuteur connecté 
""" 
class getStageTuteur(APIView):
    permission_classes = [IsAuthenticated, TuteurPermission]

    def get (self, request, format = None):
        
        serializer = StageTuteurSerializer(request.user.instance.stage_set, many = True)

        return Response(serializer.data)