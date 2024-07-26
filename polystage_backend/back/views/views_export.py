from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import EtudiantSerializer, SoutenanceSerializer
from ..models import Etudiant, Soutenance
from django.db.models import F
 
class exportNote (APIView):

    #session : id de la session
    #filiere : nom de la filiere
    #on exporte les données d'une filière passé en paramètres
    def post (self, request, format= None) :
        try:
            nom_filiere = request.data['filiere']
            id_session = request.data['session']
        except :
            return Response({'error' : "vous devez pr²éciser le nom de la filiere et l'id de la session : nom_filiere, id_session"})
        
    
        soutenances_notes = Soutenance.objects.filter(jury__session__filiere__nom = nom_filiere, jury__session__id = id_session
            ).annotate(nom = F("stage__etudiant__last_name"), prenom = F("stage__etudiant__first_name"), num_etudiant = F("stage__etudiant__num_etudiant"), num_convention = F("stage__num_convention")
            ).values("num_etudiant", "nom", "prenom", "num_convention", "note")
        
        return Response(soutenances_notes)
    