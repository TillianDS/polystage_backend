from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import EtudiantSerializer, SoutenanceSerializer
from ..models import Etudiant, Soutenance
from django.db.models import F
 
class exportNote (APIView):

    #promo : année de la promo
    #filiere : nom de la filiere
    #on exporte les données d'une filière passé en paramètres
    def post (self, request, format= None) :

        nom_filiere = request.data['filiere']
        annee_promo = request.data['promo']

        etudiants = Etudiant.objects.select_related("promo__filiere").select_related("soutenance").annotate(filiere=F("promo__filiere__nom"), note_soutenance = F("soutenance__note"), promo_annee = F("promo__annee")).filter(filiere = nom_filiere, promo__annee = annee_promo).values("num_etudiant", "first_name", "last_name", "promo_annee", "filiere", "note_soutenance")
        return Response(etudiants)
    