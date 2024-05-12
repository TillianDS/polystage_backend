from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login, authenticate


# Create your views here.   
class FiliereList(APIView):

    """
    List all code snippets, or create a new filiere.
    """
    
    def get(self, request, format=None):
        filieres = Filiere.objects.all()
        serializer = FiliereSerializer(filieres, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = FiliereSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def filiere_details(request, pk, format = None):
    """
    Retrieve, update or delete a filiere.
    """
    try:
        filiere = Filiere.objects.get(pk=pk)
    except Filiere.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FiliereSerializer(filiere)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = Response(filiere, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        filiere.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)