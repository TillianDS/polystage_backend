from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import *
from ..serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

class test(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None ):
        pk = request.data['session']
        session = Session.objects.get(pk=pk)
        soutenance = Soutenance.objects.filter(jury__session = session)
        etudiants = Etudiant.objects.filter(stage__soutenance__in = soutenance)
        serializer = EtudiantSerializer(etudiants, many=True)
        return Response(serializer.data)
    

from django.http import JsonResponse
from django.middleware.csrf import get_token

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})