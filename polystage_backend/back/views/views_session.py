from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Session
from ..serializers import SessionEtudiantSerializer
from rest_framework.authentication import TokenAuthentication
from polystage_backend.permissions import *

class getEtudiantSession(APIView):
    def get(self, request, pk, format= None ):
        try :
            session = Session.objects.get(pk=pk)
        except:
            return Response({"error':f'la session {pk} n'existe pas"})
        serializer = SessionEtudiantSerializer(session)

        return Response(serializer.data)