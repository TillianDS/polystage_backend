from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Soutenance
from ..serializers import SoutenanceSerializer
from rest_framework.authentication import TokenAuthentication
from .date_heure import getTime, getDate

class SoutenanceList(APIView):
    def get(self, request, format = None):
        soutenance = Soutenance.objects.all()
        serializer = SoutenanceSerializer(soutenance, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request, format = None):
        date_soutenance = getDate(request.data['date_soutenance'])
        time_soutenance = getTime(request.data['heure_soutenance'])

        data = request.data.copy()
        data['date_soutenance'] = date_soutenance
        data['heure_soutenance'] = time_soutenance
        serializer = SoutenanceSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SoutenanceDetails(APIView):
    def getSoutenance (self, pk):
        soutenance = Soutenance.objects.get(pk = pk)
        return soutenance
    
    def get(self, request, pk, format = None):
        soutenance =  self.getSoutenance(pk)
        serialzier = SoutenanceSerializer(soutenance)
        return Response(serialzier.data, status= status.HTTP_200_OK)
    
    def put (self, request, pk, format = None):
        soutenance = self.getSoutenance(pk)
        date_soutenance = getDate(request.data['date_soutenance'])
        time_soutenance = getTime(request.data['heure_soutenance'])

        data = request.data.copy()
        data['date_soutenance'] = date_soutenance
        data['heure_soutenance'] = time_soutenance
        serializer = SoutenanceSerializer(soutenance, data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete (self, request, pk, format = None):
        soutenance = self.getSoutenance(pk= pk)
        soutenance.delete()
        return Response({"success" : "soutenance supprimée avec succès"})