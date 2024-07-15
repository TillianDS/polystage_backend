from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Session, Jury
from ..serializers import SessionAllSerializer, JurySerializer, SessionSerializer
from rest_framework.authentication import TokenAuthentication
from polystage_backend.permissions import *

class getInfoSession(APIView):
    permission_classes = [AdminJuryPermission]

    def get(self, request, pk, format= None ):
        try :
            session = Session.objects.get(pk=pk)
        except:
            return Response({"error':f'la session {pk} n'existe pas"})
        serializer = SessionAllSerializer(session)
        return Response(serializer.data)
    
class getUserSession(APIView):
    permission_classes = [IsAuthenticated, AdminJuryPermission]

    def get(self, request, format = None):
        profile = request.user.profile
        if profile == 'ADM' :
            serializer = SessionSerializer(request.user.filiere.session_set, many = True)
        else :
            serializer = SessionSerializer(request.user.jury_set.session, many = True)
        return Response(serializer.data)

