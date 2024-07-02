from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Jury
from ..serializers import JurySerializer
from rest_framework.authentication import TokenAuthentication
from ..models import CustomUser, Enseignant, Tuteur, Admin, Professionnel, Etudiant, Session, Soutenance
from ..serializers import UserSerializer, EnseignantSerializer, TuteurSerializer, ProfessionnelSerializer, AdminSerializer, EtudiantSerializer, SessionSerializer, StageSerializer, SoutenanceSerializer, JurySerializer


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
            if ('num_etudiant' not in stage) | ('email_tuteur' not in stage):
                errors.append({"stage" : stage, "errors" : "tous les champs nécessaires n'ont pas été remplie"})
                continue
            else :
                
                email_tuteur = stage.pop('email_tuteur')
                num_etudiant = stage.pop('num_etudiant')

                try:
                    id_etudiant = Etudiant.objects.get(num_etudiant=num_etudiant).pk
                except Etudiant.DoesNotExist:
                    errors.append({"stage": stage, "errors": f"Étudiant avec numéro {num_etudiant} n'existe pas"})
                    continue

                try:
                    id_tuteur = Tuteur.objects.get(email=email_tuteur).pk
                except Tuteur.DoesNotExist:
                    errors.append({"stage": stage, "errors": f"Tuteur avec email {email_tuteur} n'existe pas"})
                    continue
                
                
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
        soutenances_data = request.data
        errors = []

        for soutenance in soutenances_data :
            if ('num_etudiant' not in soutenance) | ('num_jury' not in soutenance):
                errors.append({"stage" : soutenance, "errors" : "tous les champs nécessaires n'ont pas été remplie"})
                continue
            else :
                num_jury = soutenance.pop('num_jury')
                num_etudiant = soutenance.pop('num_etudiant')

                try:
                    etudiant = Etudiant.objects.get(num_etudiant=num_etudiant)
                except Etudiant.DoesNotExist:
                    errors.append({"soutenance": soutenance, "errors": f"Étudiant avec numéro {num_etudiant} n'existe pas"})
                    continue
                

                try:
                    soutenance_exist = Soutenance.objects.get(etudiant=etudiant)
                    errors.append({"soutenance": soutenance, "errors": f"l'étudiant {num_etudiant} a déjà une soutenance active"})
                    continue
                except Soutenance.DoesNotExist:
                    pass

                soutenance['jury'] = num_jury
                soutenance['etudiant'] = etudiant.pk
                
                serializer = StageSerializer(data=stage)

                if serializer.is_valid() : 
                    serializer.save()
                else : 
                    errors.append({"stage" : stage, "errors" : serializer.errors})
        if errors :
            return Response({"errors" : errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success" : "tous les utilisateurs ont été crées avec succès"}, status= status.HTTP_201_CREATED)

    
class importJury(APIView):
    def post (self, request, format = None):
        num_etudiant = request.data['num_etudiant']
        etudiant = Etudiant.objects.get(num_etudiant=num_etudiant)
        

        return Response(SoutenanceSerializer(soutenance_exist).data)