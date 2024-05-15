from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Filiere, Promo, Etudiant
from ..serializers import EtudiantSerializer, FiliereSerializer, PromoSerializer
from rest_framework.authentication import TokenAuthentication

class FiliereList(APIView):

    def get (self, request, format = None):
        filiere = Filiere.objects.all()
        serializer = FiliereSerializer(filiere, many = True)
        return Response(serializer.data, status= status.HTTP_200_OK)