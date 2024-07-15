from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Filiere, Session, Etudiant
from ..serializers import FiliereSerializer, SessionSerializer, SessionFiliereSerializer
from rest_framework.authentication import TokenAuthentication
from polystage_backend.permissions import *


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
    
class SessionDetails (APIView) :

    def get_session (self, pk):
        return Session.objects.get(pk = pk)

    def get (self, request, pk, format = None ) :
        promo = self.get_session(pk)
        serializer = SessionSerializer(promo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put (self, request, pk, format = None) :
        promo = self.get_session(pk)
        serializer = SessionSerializer(promo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete (self, request, pk, format = None) :
        session :Session = self.get_session(pk)
        session.delete()
        return Response ({"success" : "promo supprimée avec succès"}, status= status.HTTP_204_NO_CONTENT)
    
class SessionList (APIView) :
    def get(self, request, format = None):
        session = Session.objects.all()
        serializer = SessionSerializer(session, many= True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def post (self, request, format = None) :
        serializer = SessionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class SessionFiliere(APIView) : 
    
    def get(self, request, format = None):
        filiere = Filiere.objects.all()
        serializer = SessionFiliereSerializer(filiere, many= True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    """
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
        serializerP = SessionFiliereSerializer(data =data)

        if serializerP.is_valid():
            return Response(serializerP.data)
        return Response(serializerP.errors)
        data = request.data.copy()
        data['filiere']= 'filiere'
        #serializer = PromoSerializer(data = request.data)
        return Response({'error' : 'error'})
    """

class getSessionFiliere(APIView):
    def get(self, request, pk, format = None):
        
        filiere = Filiere.objects.get(pk=pk)
        sessions =filiere.session_set.all()
        return Response({'filiere' : FiliereSerializer(filiere).data, 'sessions' :SessionSerializer(sessions, many = True).data})
