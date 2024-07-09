from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Etudiant
from ..serializers import EtudiantAllSeralizer
from rest_framework.authentication import TokenAuthentication
from .views_list_details import List, Details

class EtudiantAll(APIView):
    def get (self, request, pk, format = None):
        try : 
            etudiant = Etudiant.objects.get(pk=pk)
        except Etudiant.DoesNotExist :
            return Response({"error" : "l'utilisateur n'existe pas"})
        serializer = EtudiantAllSeralizer(etudiant)
        return Response(serializer.data, status=status.HTTP_200_OK)

