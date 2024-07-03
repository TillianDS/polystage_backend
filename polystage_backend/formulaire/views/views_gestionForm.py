from .views_list_details import *
from ..models import Formulaire, CheckBox, Question, ResponseForm,  statusFormulaire, ResponseCheckbox
from back.models import Etudiant
from ..serializers import FormulaireSerializer, CheckboxSerializer, FormulaireAllSerializer, QuestionSerializer, ResponseSerializer, StatusFormulaireSerializer, ResponseCheckboxSerializer
from rest_framework.response import Response
from django.db.models import Q


class validateFormulaire(APIView):
    def post (self, request, format = None):
        # on cherche les questions du formulaire
        questions_data = request.data['formulaire']['question']
        id_etudiant = request.data['id_etudiant']
        id_session = request.data['formulaire']['session']

        errors = []

        #pour chaque question on va traiter sa réponse ...
        for question in questions_data:

            # ... si la question esr checkbox
            if question['type'] == 'checkbox':

                # pour chaque checkbox de la question
                for checkbox in question['checkbox']:
                    id_checkbox = checkbox['id']

                    try :
                        responseCheckbox = checkbox['response'][0]
                    except :
                        errors.append({"question" : question, "error" : "la question n'a pas de réponse"})
                        continue

                    #on ajoute l'id de la checkbox dans la réponse
                    responseCheckbox['checkbox'] = id_checkbox

                    id_checkbox = responseCheckbox.get('id')
                    if id_checkbox :
                        try :
                            responseSave = ResponseCheckbox.objects.get(pk=id_response)
                        except ResponseCheckbox.DoesNotExist:
                            errors.append({"question" : question, 'checkbox' : checkbox,  "error" : "la reponse checkbox ayant cet id n'existe pas"})
                            continue
                        serializer = ResponseCheckboxSerializer(responseSave, data = responseCheckbox)
                    else :
                        serializer = ResponseCheckboxSerializer(data = responseCheckbox)

                    if serializer.is_valid():
                        serializer.save()
                    else :
                        errors.append({"error" : serializer.errors, 'reponse' : responseCheckbox})
            
            
            # ... si la question est d'un autre type
            else :
                id_question = question['id']

                try :
                    responseForm = question['responses'][0]
                except :
                    errors.append({"question" : question, "error" : "la question n'a pas de réponse"})
                    continue

                #on ajoute l'id de la question dans la réponse
                responseForm['question']=id_question

                id_response = responseForm.get('id')
                if id_response :
                    try :
                        responseSave = ResponseForm.objects.get(pk=id_response)
                    except ResponseForm.DoesNotExist:
                        errors.append({"question" : question, "error" : "la reponse ayant cet id n'existe pas"})
                        continue
                    serializer = ResponseSerializer(responseSave, data = responseForm)
                else :
                    serializer = ResponseSerializer(data = responseForm)

                if serializer.is_valid():
                    serializer.save()
                else :
                    errors.append({"error" : serializer.errors, 'reponse' : responseForm})
        
        if errors:
            return Response({"error" : errors, "message" : "ces questions ont recontrés des erreurs et n'ont pas été enregistré"})

        status = {'etudiant' : id_etudiant, "session" : id_session, 'statutsForm' : 'rendu'}
        serializer = StatusFormulaireSerializer
        return Response({"sucess" :"tout a été enregistré avec succès"})
    
class saveFormulaire (APIView):
    def post (self, request, format = None):
        return
    
class getStatusFormulaire(APIView):
    def post (self, request, format = None):
        id_user = request.data['id_user']
        id_formulaire = request.data['id_formulaire']
        statutForm = statusFormulaire.objects.get(formulaire = id_formulaire, user= id_user)
        return Response({"status" : statutForm.status})