from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Jury
from ..serializers import JurySerializer, JuryAffichageSerializer
from rest_framework.authentication import TokenAuthentication

class JuryList(APIView):
    def get (self, request, format = None):
        jury = Jury.objects.all()
        serializer = JuryAffichageSerializer(jury, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request, format = None):
        serializer = JurySerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JuryDetails (APIView):
    def getJury (self, pk):
        jury = Jury.objects.get(pk = pk)
        return jury
    
    def get (self, request, pk, format = None):
        jury = self.getJury(pk)
        serializer = JuryAffichageSerializer(jury)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put (self, request, pk, format = None):
        jury = self.getJury(pk)

        serializer = JurySerializer(jury, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        jury = self.getJury(pk)
        jury.delete()
        return Response({"success" : "jury supprimé avec succés"}, status = status.HTTP_200_OK)