from .views_list_details import *
from ..models import ResponseForm, Formulaire, ResponseCheckbox
from ..serializers import ResponseSerializer, FormulaireResponseSerializer, ResponseCheckboxSerializer
from rest_framework.response import Response

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

        id_etudiant = data['id_etudiant']
        id_formulaire = data['id_formulaire']

        try:
            formulaire = Formulaire.objects.get(pk=id_formulaire)
        except Formulaire.DoesNotExist:
            return Response({"error": "Formulaire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer_context = {
            'user_id': id_etudiant,
        }
        serializer = FormulaireResponseSerializer(formulaire, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)