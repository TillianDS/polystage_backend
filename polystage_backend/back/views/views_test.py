from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Soutenance
from ..serializers import SoutenanceSerializer
from rest_framework import status

class test(APIView):
    def get(self, request, format=None ):
        soutenance = Soutenance.objects.all()
        serializer = SoutenanceSerializer(soutenance, many= True)
        return Response(serializer.data)