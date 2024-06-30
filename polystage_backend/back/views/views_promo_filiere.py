from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Filiere, Promo, Etudiant
from ..serializers import FiliereSerializer, PromoSerializer, PromoFiliereSerializer
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth.decorators import login_required
from polystage_backend.permissions import RedirectUnauthenticated

class FiliereList(APIView):
    
    permission_classes = [RedirectUnauthenticated]

    def get (self, request, format = None):
        filiere = Filiere.objects.all()
        serializer = FiliereSerializer(filiere, many = True)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def post (self, request, format = None) :
        serializer = FiliereSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    
    def delete (self, request, pk, format= None):
        filiere = self.get_filiere(pk)
        filiere.delete()
        return Response ({"success" : "filiere supprimée avec succès"}, status= status.HTTP_204_NO_CONTENT)
    
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
    def get(self, request, format = None):
        promo = Promo.objects.all()
        serializer = PromoSerializer(promo, many= True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def post (self, request, format = None) :
        serializer = PromoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class PromoFiliere(APIView) : 
    
    def get(self, request, format = None):
        promo = Promo.objects.all()
        serializer = PromoFiliereSerializer(promo, many= True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    """"
    def post (self, request, format = None) : 
        data = Filiere.objects.filter(nom = request.data['nom'])

        if data :
            filiere = FiliereSerializer(request.data).data
        else : 
            serializerF = FiliereSerializer(data = request.data)
            if serializerF.is_valid():
                serializerF.save()
                filiere = serializerF.data


        data = {'annee' : request.data['annee'], 'filiere' : filiere}
        serializerP = PromoFiliereSerializer(data =data)

        if serializerP.is_valid():
            return Response(serializerP.data)
        return Response(serializerP.errors)
        data = request.data.copy()
        data['filiere']= 'filiere'
        #serializer = PromoSerializer(data = request.data)
        return Response({'error' : 'error'})
    """

class getPromoOfFiliere(APIView):
    def post(self, request, format = None):
        try :
            id_filiere = request.data["id_filiere"]
        except :
            return Response({"error" : "vous devez inclure un id_filiere"}, status = status.HTTP_400_BAD_REQUEST)
        filiere = Filiere.objects.get(pk=id_filiere)
        promos =filiere.promo_set.all()
        return Response(PromoSerializer(promos, many = True).data)
