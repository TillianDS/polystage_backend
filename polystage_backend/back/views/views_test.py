from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Jury, Enseignant, CustomUser
from ..serializers import JurySerializer, EnseignantSerializer
from rest_framework import status

class test(APIView):
    def get(self, request, format=None ):
        user = Enseignant.objects.get(pk =18)
        jury= JurySerializer(user.jury_set.all(), many = True)
        return Response({'jury':jury.data})