from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Session, Jury
from ..serializers import SessionEtudiantSerializer, JurySerializer
from rest_framework.authentication import TokenAuthentication
from polystage_backend.permissions import *

class getInfoSession(APIView):
    def get_unique_juries_for_session(self, session_id):
        session = Session.objects.get(pk=session_id)
        juries = Jury.objects.filter(
            soutenance__etudiant__sessions=session
        ).distinct()

        return juries

    def get(self, request, pk, format= None ):
        try :
            session = Session.objects.get(pk=pk)
        except:
            return Response({"error':f'la session {pk} n'existe pas"})
        serializer = SessionEtudiantSerializer(session)
        jury = self.get_unique_juries_for_session(2)
        serializer = JurySerializer(jury, many= True)
        return Response(serializer.data)