from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Etudiant
from ..serializers import EtudiantAllSeralizer
from rest_framework.authentication import TokenAuthentication
from .views_list_details import List, Details
from polystage_backend.permissions import *

class EtudiantAll(APIView):
    permission_classes = [EtuPermission]
    def get (self, request, format = None):
        serializer = EtudiantAllSeralizer(request.user.instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

