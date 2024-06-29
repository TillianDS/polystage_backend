from .views_list_details import *
from ..models import Response
from ..serializers import ResponseSerializer

class ResponseList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Response, ResponseSerializer)
        
class ResponseDetails (Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Response, ResponseSerializer, "Response")

class responseFormulaire(APIView):
    
    def post (self, request, format = None):
        data = request.data

        id_etudiant = data['id_etudiant']
        id_formulaire = data['id_formulaire']


        return Response()