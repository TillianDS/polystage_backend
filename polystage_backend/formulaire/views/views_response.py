from .views_list_details import *
from ..models import ResponseForm, Formulaire, ResponseCheckbox
from ..serializers import ResponseSerializer, FormulaireResponseSerializer, ResponseCheckboxSerializer
from rest_framework.response import Response
from back.models import Soutenance, Stage
from back.serializers import SessionSerializer, SoutenanceSerializer

class ResponseList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(ResponseForm, ResponseSerializer)
        
class ResponseDetails (Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(ResponseForm, ResponseSerializer, "Response")

class ResponseCheckboxList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(ResponseCheckbox, ResponseCheckboxSerializer)
        
class ResponseCheckboxDetails (Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(ResponseCheckbox, ResponseCheckboxSerializer, "ResponseCheckbox")

class responseFormulaire(APIView): 
    def post (self, request, format = None):
        data = request.data

        id_stage = data['id_stage']
        id_formulaire = data['id_formulaire']

        try:
            formulaire = Formulaire.objects.get(pk=id_formulaire)
        except Formulaire.DoesNotExist:
            return Response({"error": "Formulaire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer_context = {
            'id_stage': id_stage,
        }
        serializer = FormulaireResponseSerializer(formulaire, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
"""
retourne le formulaire pour l'utilisateur actuel selon le stage spécifié
"""
class formUser(APIView):
    
    def post (self, request, format = None):
        id_stage = request.data['id_stage']
        profile = request.user.profile
        try :
            stage = Stage.objects.get(pk=id_stage)
        except Stage.DoesNotExist :
            return Response({"error" : "le stage n'existe pas"})
        
        session = stage.StageSession
        if not session :
            return Response("la soutenance ou la session ne sont pas encore définies")
        
        formulaire = Formulaire.objects.filter(profile = profile, session = stage.StageSession)

        serializer_context = {
            'id_stage': id_stage,
        }
        serializer = FormulaireResponseSerializer(formulaire, context=serializer_context, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)