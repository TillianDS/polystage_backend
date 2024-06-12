from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Etudiant
from ..serializers import EtudiantAllSeralizer
from rest_framework.authentication import TokenAuthentication
from .views_list_details import List, Details

class EtudiantAll(APIView):
    def get (self, request, pk, format = None):
        etudiant = Etudiant.objects.get(pk=pk)
        serializer = EtudiantAllSeralizer(etudiant)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SoutenanceDetails(APIView):
    pass
