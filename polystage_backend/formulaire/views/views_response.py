from .views_list_details import *
from ..models import ResponseForm, Formulaire, ResponseCheckbox
from ..serializers import ResponseSerializer, FormulaireResponseSerializer, ResponseCheckboxSerializer, FormulaireSerializer
from rest_framework.response import Response
from back.models import Soutenance, Stage
from back.serializers import SessionSerializer, SoutenanceSerializer, StageSerializer
from polystage_backend.permissions import *

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


"""
renvoie un formulaire ses questions et réponses associés
"""
class responseFormulaire(APIView): 
    
    def post (self, request, format = None):
        data = request.data

        id_stage = data['id_stage']
        id_formulaire = data['id_formulaire']

        try:
            formulaire = Formulaire.objects.get(pk=id_formulaire)
        except Formulaire.DoesNotExist:
            return Response({"error": "Formulaire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        #vérification que les utilisateurs etudiant ou tuteur accède bien à leur stage associé
        try:
            stage = Stage.objects.get(pk=id_stage)
        except Stage.DoesNotExist:
            return Response({"error": "Le stage n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.verify_stage(id_stage) :
            return Response({"error": "Vous n'avez pas accès à ce stage"}, status=status.HTTP_403_FORBIDDEN)

        if (request.user.profile == 'ETU') or (request.user.profile == 'TUT'):        
            
            if not stage.soutenu and (request.user.profile != formulaire.profile): 
                return Response({'error' : "ce formulaire n'est pas encore accessible"})
            
        serializer_context = {
            'id_stage': id_stage,
        }
        serializer = FormulaireResponseSerializer(formulaire, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)
