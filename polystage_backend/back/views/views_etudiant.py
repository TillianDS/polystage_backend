from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Etudiant
from ..serializers import EtudiantSerializer
from rest_framework.authentication import TokenAuthentication


# Create your views here.   
class EtudiantList(APIView):

    """

    """
    
    def get(self, request, format=None):
        etudiant = Etudiant.objects.all()
        serializer = EtudiantSerializer(etudiant, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = EtudiantSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

