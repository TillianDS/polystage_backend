from rest_framework import status
from .views_list_details import *
from ..models import Formulaire, Question, ResponseForm,  StatusFormulaire, ResponseCheckbox
from back.models import Stage
from ..serializers import FormulaireSerializer, ResponseSerializer, ResponseCheckboxSerializer
from rest_framework.response import Response
from django.db.models import Q
from mail.views import *

"""
vérifie c
"""
def verifyFormulaire (request, id_stage, id_formulaire):
        #on vérifie que le stage existe bien
        try:
            stage = Stage.objects.get(pk=id_stage)
        except Stage.DoesNotExist:
            return Response({"error": [{'error' :"le stage n'existe pas"}]}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.verify_stage(id_stage) :
            return Response({"error": [{'error' :"Vous n'avez pas accès à ce stage"}]}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            formulaire = Formulaire.objects.get(pk=id_formulaire)
        except Formulaire.DoesNotExist:
            return Response({"error": [{'error': "le formulaire n'existe pas"}]}, status=status.HTTP_400_BAD_REQUEST)
        
        if formulaire.profile == 'JURY' :
            if((request.user.profile != 'PRO') or (request.user.profile != 'ENS')):
                return Response({"error": [{'error' : "Vous ne pouvez pas répondre à ce formulaire"}]})
        else:
            if formulaire.profile != request.user.profile :
                return Response({"error": [{'error' : "Vous ne pouvez pas répondre à ce formulaire"}]})

            statusForm = StatusFormulaire.objects.get(stage = stage, user = request.user, formulaire = id_formulaire)

            if statusForm.is_rendu:
                return Response({'error' : [{'error' : "le formulaire a déjà été rendu"}]}, status=status.HTTP_403_FORBIDDEN)
        
        return formulaire.titre
"""
vérifie que toutes les questions du formulaire sont bien renseigné
"""
def verifyQuestion (request, questions, id_formulaire) :
    questionForm = Question.objects.filter(formulaire = id_formulaire )
    questionSearchs = []

    for question in questions :
        try :
            questionSearch = Question.objects.get(pk =question['id'], formulaire = id_formulaire)
        except Question.DoesNotExist :
            return Response({'error' : [{'error' : f"la question avec l'id {question["id"]} n'existe pas dans le formulaire {id_formulaire} "}]})

        questionSearchs.append(questionSearch)
    
    for question in questionForm :
        if question not in questionSearchs:
            return Response({'error' : [{'error' : "Vous deviez spécifier toutes les question du formulaire"}]})
    return True

class saveFormulaire (APIView):
    def post (self, request, format = None):
        # on cherche les questions du formulaire
        questions_data = request.data['formulaire']['question']
        id_stage = request.data['id_stage']
        id_formulaire = request.data['formulaire']['id']

        errors = []
        titre_form = verifyFormulaire(request, id_stage=id_stage, id_formulaire=id_formulaire)
        if isinstance(titre_form, Response):
            return titre_form
        
        verifyQ =  verifyQuestion(request, questions_data, id_formulaire)
        if verifyQ != True :
            return verifyQ
        
        #pour chaque question on va traiter sa réponse ...
        for question in questions_data:

            # ... si la question esr checkbox
            if question['type'] == 'checkbox':

                # pour chaque checkbox de la question
                for checkbox in question['checkbox']:
                    id_checkbox = checkbox['id']

                    try :
                        responseCheckbox = checkbox['response']
                    except :
                        continue

                    #on ajoute l'id de la checkbox dans la réponse
                    responseCheckbox['checkbox'] = id_checkbox
                    #on ajoute l'id du stage dans la réponse
                    responseCheckbox['stage'] = id_stage

                    try :
                        responseSave = ResponseCheckbox.objects.get(checkbox = id_checkbox, stage = id_stage)
                        serializer = ResponseCheckboxSerializer(responseSave, data = responseCheckbox)
                    
                    except ResponseCheckbox.DoesNotExist:
                        serializer = ResponseCheckboxSerializer(data = responseCheckbox)

                    if serializer.is_valid():
                        serializer.save()
                    else :
                        errors.append({"error" : serializer.errors, 'reponse' : responseCheckbox})
            
            
            # ... si la question est d'un autre type
            else :
                id_question = question['id']

                #on cheche la réponse à la question
                try :
                    responseForm = question['response']
                except :
                    # si elle n'exsite pas on passe à la question d'aprés
                    continue

                #on ajoute l'id de la question dans la réponse
                responseForm['question']=id_question
                #on ajoute l'id du stage dans la réponse
                responseForm['stage'] = id_stage

                try :
                    responseSave = ResponseForm.objects.get(question = id_question, stage = id_stage)
                    serializer = ResponseSerializer(responseSave, data = responseForm)
                except ResponseForm.DoesNotExist:
                    serializer = ResponseSerializer(data = responseForm)

                if serializer.is_valid():
                    serializer.save()
                else :
                    errors.append({"error" : serializer.errors, 'reponse' : responseForm})
        
        statusForm = StatusFormulaire.objects.get(stage = id_stage, user = request.user, formulaire = id_formulaire)
        
        statusForm.statusForm = 'sauvegarde'
        statusForm.save()

        if errors:
            return Response({"error" : errors, "message" : "ces questions ont recontrés des erreurs et n'ont pas été enregistré"})
        
        mailSauvegardeForm("tillian.dhume@laposte.net", titre_form)

        try :
            mailSauvegardeForm("tillian.dhume@laposte.net", titre_form)
        except :
            pass
        return Response({"sucess" :"tout a été enregistré avec succès"}) 
 
class validateFormulaire(APIView):
    
    def post (self, request, format = None):
        # on cherche les questions du formulaire
        questions_data = request.data['formulaire']['question']
        id_stage = request.data['id_stage']
        id_formulaire = request.data['formulaire']['id']

        errors = []

        verifyQ =  verifyQuestion(request, questions_data, id_formulaire)
        if verifyQ != True :
            return verifyQ

        errors = []
        titre_form = verifyFormulaire(request, id_stage=id_stage, id_formulaire=id_formulaire)
        if isinstance(titre_form, Response):
            return titre_form
        
        #pour chaque question on va traiter sa réponse ...
        for question in questions_data:
            id_question = question['id']

            # ... si la question esr checkbox
            if question['type'] == 'checkbox':

                # pour chaque checkbox de la question
                for checkbox in question['checkbox']:
                    id_checkbox = checkbox['id']

                    

                    question_save = Question.objects.get(pk = id_question)
                    try :
                        responseCheckbox = checkbox['response']
                    except :
                        if question_save.obligatoire :
                            errors.append({"question" : question, "error" : "la question n'a pas de réponse"})
                        continue

                    #on ajoute l'id de la checkbox dans la réponse
                    responseCheckbox['checkbox'] = id_checkbox
                    responseCheckbox['stage']=id_stage

                    try :
                        responseSave = ResponseCheckbox.objects.get(checkbox = id_checkbox, stage = id_stage)
                        serializer = ResponseCheckboxSerializer(responseSave, data = responseCheckbox)
                    
                    except ResponseCheckbox.DoesNotExist:
                        serializer = ResponseCheckboxSerializer(data = responseCheckbox)

                    if serializer.is_valid():
                        serializer.save()
                    else :
                        errors.append({"error" : serializer.errors, 'reponse' : responseCheckbox})
            
            
            # ... si la question est d'un autre type
            else :

                question_save = Question.objects.get(pk = id_question)

                try :
                    responseForm = question['response']
                except :
                    if question_save.obligatoire :
                        errors.append({"question" : question, "error" : "la question n'a pas de réponse"})
                    continue

                #on ajoute l'id de la question dans la réponse
                responseForm['question']=id_question
                responseForm['stage']=id_stage

                try :
                    responseSave = ResponseForm.objects.get(question = id_question, stage = id_stage)
                    serializer = ResponseSerializer(responseSave, data = responseForm)
                except ResponseForm.DoesNotExist:
                    serializer = ResponseSerializer(data = responseForm)

                if serializer.is_valid():
                    serializer.save()
                else :
                    errors.append({"error" : serializer.errors, 'reponse' : responseForm})
        
        if errors:
            return Response({"error" : errors, "message" : "ces questions ont recontrés des erreurs et n'ont pas été enregistré"})

        statusForm = StatusFormulaire.objects.get(stage = id_stage, user = request.user, formulaire = id_formulaire)
        
        statusForm.statusForm = 'rendu'
        statusForm.save()

        try :
            mailConfirmationForm(request.user.email, titre_form)
        except :
            pass
        return Response({"sucess" :"le formulaire a été enregistré avec succés"}) 
   

"""
permet de rechercher un formulaire selon son titre, sa description, le rôle à qui il s'adresse, sa filière
"""  
class FormulaireSearch (APIView):
    def post(self, request, format = None):
        search = request.data['search']

        formulaire = Formulaire.objects.filter(Q(titre__icontains = search) |
                                           Q(profile__icontains = search) | 
                                           Q(description__icontains = search) | 
                                           Q(filiere__nom__icontains = search))
        
        return Response(FormulaireSerializer(formulaire, many = True).data)