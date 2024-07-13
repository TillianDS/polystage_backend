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
    def choose_user (self, profile, email):
        if profile == 'ENS' : 
            return Enseignant.objects.get(email =email)
        elif profile == 'ETU':
            return Etudiant.objects.get(email = email)
        elif profile == 'PRO':
            return Professionnel.objects.get(email = email)
        elif profile == 'TUT':
            return Tuteur.objects.get(email = email)
        
    def get(self, request, format=None ):
        try :
            etudiant = self.choose_user('ETU', 'etudee@po.fr')
            serializer = EtudiantSerializer(etudiant)
        except :
            return Response(serializer.data)
    

from django.http import JsonResponse
from django.middleware.csrf import get_token

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})