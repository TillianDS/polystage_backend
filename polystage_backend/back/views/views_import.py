from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Jury
from ..serializers import JurySerializer
from rest_framework.authentication import TokenAuthentication
from ..models import CustomUser, Enseignant, Tuteur, Admin, Professionnel, Etudiant, Promo
from ..serializers import UserSerializer, EnseignantSerializer, TuteurSerializer, ProfessionnelSerializer, AdminSerializer, EtudiantSerializer, PromoSerializer, StageSerializer, SoutenanceSerializer, JurySerializer


class importUser (APIView):
        
    def choose_deserializer (self, profile, user) :
        if profile == 'ENS' : 
            return EnseignantSerializer(data =user)
        elif profile == 'ETU':
            return EtudiantSerializer(data = user)
        elif profile == 'ADM':
            return AdminSerializer(data =user)
        elif profile == 'PRO':
            return ProfessionnelSerializer(data = user)
        elif profile == 'TUT':
            return TuteurSerializer(data = user)
        else :
            return 'error'
          
    def choose_user (self, profile):
        if profile == 'ENS' : 
            return Enseignant.objects.all()
        elif profile == 'ETU':
            return Etudiant.objects.all()
        elif profile == 'ADM':
            return Admin.objects.all()
        elif profile == 'PRO':
            return Professionnel.objects.all()
        elif profile == 'TUT':
            return Tuteur.objects.all()

    def post (self, request, format = None) :

        users_data = request.data

        errors = []
        for user in users_data :
            serializer = self.choose_deserializer(user= user, profile= user["profile"])
            if serializer.is_valid() : 
                serializer.save()
            else : 
                errors.append({"user" : user, "errors" : serializer.errors})
        if errors :
            return Response({"errors" : errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success" : "tous les utilisateurs ont été crées avec succès"}, status= status.HTTP_201_CREATED)

""""
class importPromoFiliere(APIView) :

    def post (self, request, format = None):
        promoFiliereData = request.data

        errors = []

        for promFil in promoFiliereData: 
            serializer = promofil
        return Response()
"""

"""
import en masse de stage, pour les tuteur on précisera seulement leur adresse mai let les étudiants leur numéro étudiant
"""
class importStage (APIView):
    def post(self, request, format = None):
        stages_data = request.data
        errors = []

        for stage in stages_data :
            email_tuteur = stage.pop('email_tuteur')
            num_etudiant = stage.pop('num_etudiant')

            id_etudiant = Etudiant.objects.get(num_etudiant= num_etudiant) .pk
            id_tuteur = Tuteur.objects.get(email = email_tuteur).pk

            stage['tuteur'] = id_tuteur
            stage['etudiant'] = id_etudiant
            
            serializer = StageSerializer(data=stage)

            if serializer.is_valid() : 
                serializer.save()
            else : 
                errors.append({"stage" : stage, "errors" : serializer.errors})
        if errors :
            return Response({"errors" : errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success" : "tous les utilisateurs ont été crées avec succès"}, status= status.HTTP_201_CREATED)

    
class importSoutenance(APIView):
    def post (self, request, format = None):
        tuteurs = Tuteur.objects.get(pk=3)

        
        return Response({'id':tuteurs.jurys.all()})
    
class importJury(APIView):
    def post (self, request, format = None):
        return Response()