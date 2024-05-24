from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Question
from ..serializers import QuestionSerializer


class QuestionList(APIView):

    def get (self, request, format = None):
        formulaire = Question.objects.all()
        serializer = QuestionSerializer(formulaire, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request, format = None):
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class QuestionDetails(APIView):
    def getFormulaire (self, pk):
        return Question.objects.get(pk = pk)
    
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