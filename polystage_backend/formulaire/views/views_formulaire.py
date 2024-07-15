from .views_list_details import *
from ..models import Formulaire, CheckBox, Question
from back.models import Session, Stage
from back.serializers import SoutenanceSerializer

from ..serializers import FormulaireSerializer, CheckboxSerializer, FormulaireAllSerializer, QuestionSerializer
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from polystage_backend.permissions import *

# définition des class pour la gestion des formulaires uniquement
class FormulaireList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Formulaire, FormulaireSerializer)

class FormulaireDetails(Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Formulaire, FormulaireSerializer, "Formulaire")


# définition des class pour la gestion des questions uniquement
class QuestionList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Question, QuestionSerializer)
        
class QuestionDetails (Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Question, QuestionSerializer, "Question")


# définition des class pour la gestion des checkbox uniquement
class CheckboxList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(CheckBox, CheckboxSerializer)

class CheckboxDetails(Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(CheckBox, CheckboxSerializer, "Checkbox")


# définition des class pour la création de formulaire, question et checkbox en même temps
class CreateFormulaireAll(APIView):
    permission_classes = [IsAuthenticated, AdminPermission]
    def post(self, request, format= None):
        id_session = request.data.get('session')
        if not id_session :
            return Response({'error' : "le formulaire doit être associé à une session"})

        try : 
            session = Session.objects.get(pk=id_session)
        except Session.DoesNotExist :
            return Response({'error' : f"la session avec l'id {id_session} n'existe pas"})

        #on vérifie que l'administratuer à bien accès à la session associé au formulaire
        if session.filiere != request.user.filiere :
            return Response({"error" :"vous n'êtes pas autorisé à créer un formulaire pour cette session"})
        
        serializer = FormulaireAllSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModifyFormulaireAll(APIView):
    permission_classes = [IsAuthenticated, AdminPermission]

    def put (self, request, pk, format = None):

        id_formulaire = pk
        questions = request.data.pop('question', None)

        id_session = request.data.get('session')
        if not id_session :
            return Response({'error' : "le formulaire doit être associé à une session"})

        if questions == None:
            return Response({'error' : "il manque le champ questions"}, status=status.HTTP_400_BAD_REQUEST)

        try :
            formulaire_save = Formulaire.objects.get(pk=id_formulaire)
        except Formulaire.DoesNotExist:
            return Response({'error' : f"le formulaire avec l'id {id_formulaire} n'exsite pas"}, status=status.HTTP_400_BAD_REQUEST)

        if formulaire_save.session.filire.id !=  id_session :
            return Response({'error' : "vous ne pouvez pas changer ce formulaire de session"})
        
        serializer = FormulaireSerializer(request.data, data = formulaire_save)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        formulaire_save = serializer.save()

        errors = []
        for question in questions :
            question['formulaire'] = id_formulaire
            id_question = question.get('id')

            checkboxs_data = question.pop('checkbox', None)
            if checkboxs_data == None :
                errors.append({'question' : question, 'error' : "la question n'a pas de checkbox : checkbox : []"})
                continue
        
            if not id_question :
                serializer = QuestionSerializer(data = question)
            else :
                try :
                    question_save = Question.objects.get(pk=id_question)
                except Question.DoesNotExist :
                    errors.append({'question' : question, 'error' : f"la question avec l'id {id_question} n'existe pas"})
                    continue
                
                serializer = QuestionSerializer(question_save, data = question)
                if not serializer.is_valid():
                    errors.append({'question' : question, 'error' : serializer.errors})
                    continue
                question_save = serializer.save()

                id_question = question_save.id

            if question['type']== 'checkbox' :
                for checkbox in checkboxs_data :
                    checkbox['question'] = id_question
                    id_checkbox = checkbox.get('id')
                    if id_checkbox :
                        try :
                            checkbox_save = CheckBox.objects.get(pk = id_checkbox)
                        except CheckBox.DoesNotExist :
                            errors.append({'question' : question, 'checkbox' :checkbox, 'error' : f"la checkbox avec l'id {id_checkbox} n'exsite pas"})
                            continue

                        serializer = CheckboxSerializer(checkbox_save, data = checkbox)
                    else :
                        serializer = CheckboxSerializer(data = checkbox)
                if not serializer.is_valid():
                    errors.append({'question' : question, 'checkbox' :checkbox, 'error' : serializer.errors})
                    continue
                serializer.save()
                            
        if errors :
            return Response({'errors' : errors})
        return Response(FormulaireAllSerializer(formulaire_save).data)
  
"""
retourne toutes les informations d'un formulaire
"""
class GetFormulaireAll(APIView):
    permission_classes = [IsAuthenticated, AdminPermission]
    def get(self, request, pk, format= None):
        formulaire = Formulaire.objects.get(pk=pk)
        serializer = FormulaireAllSerializer(formulaire)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
retourne le formulaire pour l'étudiant ou le tuteur connecté selon le stage spécifié, 
si le stage a été soutenu, cela renvoie tous les formulaires associés
"""
class formUser(APIView):
    
    def post (self, request, format = None):
        id_stage = request.data['id_stage']
        profile = request.user.profile

        try :
            stage = Stage.objects.get(pk=id_stage)
        except Stage.DoesNotExist :
            return Response({"error" : "le stage n'existe pas"})
        

        #vérification que les utilisateurs etudiant ou tuteur accède bien à leur stage associé
        if not request.user.verify_stage(id_stage):
            return Response({"error": "Vous n'avez pas accès à ce stage"}, status=status.HTTP_403_FORBIDDEN)
        
        #on récupère la session du stage
        session = stage.StageSession
        if not session :
            return Response("la soutenance ou la session ne sont pas encore définies")
        
    
        if stage.soutenu or (profile == 'ENS') or (profile == 'PRO')  or (profile == 'ADM'):
            formulaire = Formulaire.objects.filter(session = stage.StageSession)
        else :
            formulaire = Formulaire.objects.filter(profile = profile, session = stage.StageSession)

        serializer = FormulaireSerializer(formulaire, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)