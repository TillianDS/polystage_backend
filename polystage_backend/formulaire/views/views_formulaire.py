from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Formulaire
from ..serializers import FormulaireSerializer

class FormulaireList(APIView):

    def get (self, request, format = None):
        formulaire = Formulaire.objects.all()
        serializer = FormulaireSerializer(formulaire, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request, format = None):
        serializer = FormulaireSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FormulaireDetails(APIView):
    def getFormulaire (self, pk):
        return Formulaire.objects.get(pk = pk)
    
    def get (self, request, pk, format = None):
        formulaire = self.getFormulaire(pk)
        serializer = FormulaireSerializer(formulaire)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put (self, request, pk, format = None):
        formulaire = self.getFormulaire(pk)
        serializer = FormulaireSerializer(formulaire, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        formulaire = self.getFormulaire(pk)
        formulaire.delete()
        return Response({'success': 'formulaire supprimé avec suucès'})