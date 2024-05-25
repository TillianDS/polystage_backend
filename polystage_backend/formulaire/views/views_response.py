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