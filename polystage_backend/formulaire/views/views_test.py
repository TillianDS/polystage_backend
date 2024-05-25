from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .views_list_details import *
from ..models import Question, Formulaire
from ..serializers_test import QuestionSerializer, FormulaireSerializer

class testList(APIView):
        
    def get (self, request, format = None):
        formulaire = Formulaire.objects.all()
        serializer = FormulaireSerializer(formulaire, many = True)
        return Response(serializer.data)
    
    def post (self, request, format = None):
        serializer = FormulaireSerializer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)