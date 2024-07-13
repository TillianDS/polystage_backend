from .views_list_details import *
from ..models import Formulaire, CheckBox, Question
from back.models import Etudiant, Stage
from back.serializers import SoutenanceSerializer

from ..serializers import FormulaireSerializer, CheckboxSerializer, FormulaireAllSerializer, QuestionSerializer
from rest_framework.response import Response
from django.db.models import Q

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
    def post(self, request, format= None):
        serializer = FormulaireAllSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class GetFormulaireAll(APIView):
    permission_classes = [AdminPermission]
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