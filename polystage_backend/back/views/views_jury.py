from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Jury
from ..serializers import JurySerializer
from rest_framework.authentication import TokenAuthentication

class JuryList(APIView):
    def get (self, request, format = None):
        jury = Jury.objects.all()
        serializer = JurySerializer(jury, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request, format = None):
        
        JurySerializer