from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Soutenance
from ..serializers import SoutenanceSerializer
from rest_framework.authentication import TokenAuthentication
from .views_list_details import List, Details

class SoutenanceList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Soutenance, SoutenanceSerializer)


class SoutenanceDetails(Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Soutenance, SoutenanceSerializer, "Soutenance")

