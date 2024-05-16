from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Filiere, Promo, Etudiant
from ..serializers import EtudiantSerializer, FiliereSerializer, PromoSerializer
from rest_framework.authentication import TokenAuthentication

class FiliereList(APIView):

    def get (self, request, format = None):
        filiere = Filiere.objects.all()
        serializer = FiliereSerializer(filiere, many = True)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def post (self, request, format = None) :
        serializer = FiliereSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class FiliereDetails (APIView):

    def get_filiere (self, pk):
        return Filiere.objects.get(pk = pk)
    
    def get (self, request, pk, format = None ) :
        filiere = self.get_filiere(pk)
        serializer = FiliereSerializer(filiere)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format= None):
        filiere = self.get_filiere(pk)
        serializer = FiliereSerializer(filiere, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete (self, request, format= None):
        return
    
class PromoDetails (APIView) :

    def get_promo (self, pk):
        return Promo.objects.get(pk = pk)

    def get (self, request, pk, format = None ) :
        promo = self.get_promo(pk)
        serializer = PromoSerializer(promo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put (self, request, pk, format = None) :
        promo = self.get_promo(pk)
        serializer = PromoSerializer(promo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete (self, request, pk, format = None) :
        promo = self.get_promo(pk)
        promo.delete()
        return Response ({"success" : "promo supprimée avec succès"}, status= status.HTTP_204_NO_CONTENT)
    
class PromoList (APIView) :
    def post (self, request, format = None) :
        serializer = PromoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
