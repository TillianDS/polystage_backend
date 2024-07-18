from .views_list_details import *
from ..models import StatusFormulaire
from ..serializers import StatusFormulaireSerializer
from rest_framework.response import Response


# définition des class pour la gestion des formulaires uniquement
class statutsFormulaireList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(StatusFormulaire, StatusFormulaireSerializer)

class statusFormulaireDetails(Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(StatusFormulaire, StatusFormulaireSerializer, "statusFormulaire")

class getStatusFormulaire(APIView):
    def post (self, request, format = None):
        try :
            id_user = request.data['id_user']
        except :
            return Response({'error' :"vous devez spécifier l'id de l'utilisateur"})
        try :
            id_formulaire = request.data['id_formulaire']
        except :
            return Response({'error' :"vous devez spécifier l'id du formulaire"})

        statutForm = StatusFormulaire.objects.get(formulaire = id_formulaire, user= id_user)
        if statutForm :
            return Response({"status" : statutForm.statusForm})
        return Response({"error" : "il n'y pas de status pour cet utilisateur et ce formulaire"})
        
    
