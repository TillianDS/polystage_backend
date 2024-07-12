from rest_framework import status
from .views_list_details import *
from ..models import Formulaire, CheckBox, Question, ResponseForm,  statusFormulaire, ResponseCheckbox
from back.models import Etudiant, Stage
from ..serializers import FormulaireSerializer, CheckboxSerializer, FormulaireAllSerializer, QuestionSerializer, ResponseSerializer, StatusFormulaireSerializer, ResponseCheckboxSerializer
from rest_framework.response import Response
from django.db.models import Q

def verifyFormulaire (request, id_stage):
        id_formulaire = request.data['formulaire']['id']

        try:
            stage = Stage.objects.get(pk=id_stage)
        except Stage.DoesNotExist:
            return Response({"error": "le stage n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.verify_stage(id_stage) :
            return Response({"error": "Vous n'avez pas accès à ce stage"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            formulaire = Formulaire.objects.get(pk=id_formulaire)
        except Formulaire.DoesNotExist:
            return Response({"error": "le formulaire n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)
        
        if formulaire.profile != request.user.profile :
            return Response({"error": "Vous ne pouvez pas répondre à ce formulaire"})

        statusForm = statusFormulaire.objects.get(stage = stage, user = request.user, formulaire = id_formulaire)

        if statusForm.is_rendu:
            return Response({'error' : "le formulaire a déjà été rendu"}, status=status.HTTP_403_FORBIDDEN)
        
        return True

class validateFormulaire(APIView):
    
    def post (self, request, format = None):
        # on cherche les questions du formulaire
        questions_data = request.data['formulaire']['question']
        id_stage = request.data['id_stage']
        id_session = request.data['formulaire']['session']
        errors = []

        verify = verifyFormulaire(request, id_stage=id_stage)
        if verify != True :
            return verify
        
        #pour chaque question on va traiter sa réponse ...
        for question in questions_data:

            # ... si la question esr checkbox
            if question['type'] == 'checkbox':

                # pour chaque checkbox de la question
                for checkbox in question['checkbox']:
                    id_checkbox = checkbox['id']
                    question_save = Question.objects.get(question['id'])
                    
                    try :
                        responseCheckbox = checkbox['response'][0]
                    except :
                        if question_save.obligatoire :
                            errors.append({"question" : question, "error" : "la question n'a pas de réponse"})
                        continue

                    #on ajoute l'id de la checkbox dans la réponse
                    responseCheckbox['checkbox'] = id_checkbox

                    id_checkboxRes = responseCheckbox.get('id')
                    if id_checkboxRes :
                        try :
                            responseSave = ResponseCheckbox.objects.get(pk=id_checkboxRes)
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

                question_save = Question.objects.get(id_question)

                try :
                    responseForm = question['responses'][0]
                except :
                    if question_save.obligatoire :
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

        status = {'stage' : id_stage, "session" : id_session, 'statutsForm' : 'sauvegarde'}
        serializer = StatusFormulaireSerializer(data= status)
        if serializer.is_valide :
            serializer.save()
            return Response({"sucess" :"tout a été enregistré avec succès"}) 
        return Response(serializer.errors)
    
class saveFormulaire (APIView):
    def post (self, request, format = None):
        # on cherche les questions du formulaire
        questions_data = request.data['formulaire']['question']
        id_stage = request.data['id_stage']
        id_session = request.data['formulaire']['session']

        errors = []

        verify = verifyFormulaire(request, id_stage=id_stage)
        if verify != True :
            return verify
        
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
                        continue

                    #on ajoute l'id de la checkbox dans la réponse
                    responseCheckbox['checkbox'] = id_checkbox

                    id_checkboxRes = responseCheckbox.get('id')
                    if id_checkboxRes :
                        try :
                            responseSave = ResponseCheckbox.objects.get(pk=id_checkboxRes)
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

        statusForm = {'stage' : id_stage, "session" : id_session, 'statutsForm' : 'sauvegarde'}
        serializer = StatusFormulaireSerializer(data= status)
        if serializer.is_valide :
            serializer.save()
            return Response({"sucess" :"tout a été enregistré avec succès"}) 
        return Response(serializer.errors)
    
class getStatusFormulaire(APIView):
    def post (self, request, format = None):
        id_user = request.data['id_user']
        id_formulaire = request.data['id_formulaire']
        statutForm = statusFormulaire.objects.get(formulaire = id_formulaire, user= id_user)
        return Response({"status" : statutForm.status})