from .views_list_details import *
from ..models import Formulaire, CheckBox, Question, ResponseForm
from back.models import Etudiant
from ..serializers import FormulaireSerializer, CheckboxSerializer, FormulaireAllSerializer, QuestionSerializer, ResponseSerializer
from rest_framework.response import Response
from django.db.models import Q


class validateFormulaire(APIView):
    def post (self, request, format = None):
        questions_data = request.data['formulaire']['question']
        errors = []
        for question in questions_data:
            if question['type'] == 'checkbox':
                for response in question['response']:
                    pass
            else :
                id_question = question['id']
                responseForm = question['responses'][0]
                responseForm['question']=id_question

                id_response = question.get('id')
                if responseForm :
                    responseSave = ResponseForm.objects.get(pk=id_response)
                    serializer = ResponseSerializer(responseSave, data = responseForm)
                else :
                    serializer = ResponseSerializer(data = responseForm)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else :
                    errors.append({"error" : serializer.errors, 'reponse' : responseForm})
        return Response(errors)
        
        #return Response(questions_data)
    
class saveFormulaire (APIView):
    def post (self, request, format = None):
        return