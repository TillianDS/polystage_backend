from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from ..models import CustomUser, Enseignant, Tuteur, Admin, Professionnel, Etudiant, Session, Soutenance,Stage, Jury, MembreJury
from ..serializers import UserSerializer, EnseignantSerializer, TuteurSerializer, ProfessionnelSerializer, AdminSerializer, EtudiantSerializer, SessionSerializer, StageSerializer, SoutenanceSerializer, FiliereSerializer,JuryImportSerializer
from polystage_backend.permissions import *

class importUser (APIView):
    permission_classes = [IsAuthenticated, AdminPermission]
    def choose_deserializer (self, profile, user) :
        if profile == 'ENS' : 
            return EnseignantSerializer(data =user)
        elif profile == 'ETU':
            return EtudiantSerializer(data = user)
        elif profile == 'PRO':
            return ProfessionnelSerializer(data = user)
        elif profile == 'TUT':
            return TuteurSerializer(data = user)
        else :
            return 'error'
        
    def choice_modify_deserializer (self, profile, user, data) :
        if profile == 'ENS' : 
            return EnseignantSerializer(user,data =data)
        elif profile == 'ETU':
            return EtudiantSerializer(user,data = data)
        elif profile == 'PRO':
            return ProfessionnelSerializer(user,data = data)
        elif profile == 'TUT':
            return TuteurSerializer(user, data = user)
        else :
            return 'error'
          
    def choose_user (self, profile, email):
        if profile == 'ENS' : 
            return Enseignant.objects.get(email =email)
        elif profile == 'ETU':
            return Etudiant.objects.get(email = email)
        elif profile == 'PRO':
            return Professionnel.objects.get(email = email)
        elif profile == 'TUT':
            return Tuteur.objects.get(email = email)
        else :
            return 'error'

    def post (self, request, format = None) :

        users_data = request.data

        errors = []
        for user in users_data :
            profile_accept = ['ETU', 'TUT', 'PRO', 'ENS']

            profile= user.get("profile")
            if not profile :
                errors.append({'user' : user, 'error' : "vous devez spécifier un profile à l'utilisateur : ETU, TUT, ENS, PRO"})
                continue

            if (profile == 'ADM') or (profile == 'SPR'):
                errors.append({'user' : user, 'error' : "vous n'êtes pas autorisé à importer des administrateurs ou des super utlisateurs"})
                continue

            elif profile not in profile_accept :
                errors.append({'user' : user, 'error' : "le profile n'est pas bon, les profiles acceptés sont les suivants : ETU, TUT, ENS, PRO"})
                continue

            try : 
                email = user['email']
                user_save = CustomUser.objects.get(email =email)

                if user_save.profile != user['profile'] :
                    errors.append({"user" : user, 'error' : "un utilisateur avec cette adresse mail existe déjà sous un autre profile"})
                    continue

            except CustomUser.DoesNotExist : 
                pass 
            
            try : 
                user_save = self.choose_user(profile=profile, email=email)
                serializer = self.choice_modify_deserializer(profile, user=user_save, data=user)
            except :
                serializer = self.choose_deserializer(user= user, profile= profile)

            if serializer == 'error' : 
                errors.append({"user" :user, "errors" :"le profile n'est pas valide"})
                continue

            if serializer.is_valid() : 
                serializer.save()
                pass
            else : 
                errors.append({"user" : user, "errors" : serializer.errors})
                continue

        if errors :
            return Response({"errors" : errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success" : "tous les utilisateurs ont été crées avec succès"}, status= status.HTTP_201_CREATED)

"""       
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
    permission_classes = [IsAuthenticated, AdminPermission]
    def post(self, request, format = None):
        stages_data = request.data
        errors = []

        for stage in stages_data :
            
            num_convention = stage.get('num_convention')
            if not num_convention :
                errors.append({"stage" : stage, "errors" : "le stage doit avoir un numero de convention : num_convention"})
                continue

            email_tuteur = stage.pop('email_tuteur', None)
            if not email_tuteur :
                errors.append({"stage" : stage, "errors" : "le stage doit avoir un email de tuteur : email_tuteur"})
                continue

            num_etudiant = stage.pop('num_etudiant', None)
            if not num_etudiant :
                errors.append({"stage" : stage, "errors" : "le stage doit avoir un numéro étudiant : num_etudiant"})
                continue

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

            try :
                stage_save = Stage.objects.get(num_convention = num_convention)
                if stage_save.etudiant.num_etudiant != num_etudiant :
                    errors.append({"stage": stage, "errors": f"Un stage avec le numero de convention : {num_convention}, existe deja pour un autre etudiant"})
                    continue
    
                serializer = StageSerializer(stage_save, data=stage )
            except Stage.DoesNotExist :
                serializer = StageSerializer(data=stage)

            if serializer.is_valid() : 
                serializer.save()
                continue
            errors.append({"stage" : stage, "errors" : serializer.errors})
           
        if errors :
            return Response({"errors" : errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success" : "tous les utilisateurs ont été crées avec succès"}, status= status.HTTP_201_CREATED)

class importSoutenance(APIView):
    permission_classes = [IsAuthenticated, AdminPermission]
    def post (self, request, format = None):
        soutenances_data = request.data
        errors = []

        filiere = request.user.instance.filiere
        for soutenance in soutenances_data :

            num_convention = soutenance.get('num_convention')
            if not num_convention :
                errors.append({"stage" : soutenance, "errors" : "la soutenance doit avoir un numero de convention"})
                continue

            nom_session = soutenance.get('nom_session')
            if not nom_session :
                errors.append({"stage" : soutenance, "errors" : "la soutenance doit avoir un nom de session"})
                continue
            
            num_jury = soutenance.get('num_jury')
            if not num_jury :
                errors.append({"stage" : soutenance, "errors" : "la soutenance doit avoir un jury : num_jury"})
                continue

            try:
                session = Session.objects.get(nom = nom_session, filiere = filiere)
            except Session.DoesNotExist:
                errors.append({"soutenance": soutenance, "errors": f"La session avec nom_session : {nom_session} n'existe pas"})
                continue
            
            try:
                jury = Jury.objects.get(num_jury = num_jury, session = session)
            except Jury.DoesNotExist:
                errors.append({"soutenance": soutenance, "errors": f"Le jury avec le num_jury : {num_jury} n'existe pas dans la session {nom_session}"})
                continue

            soutenance['jury'] = jury.id

            try:
                stage = Stage.objects.get(num_convention = num_convention)
            except Stage.DoesNotExist:
                errors.append({"soutenance": soutenance, "errors": f"Stage avec num_convention : {num_convention} n'existe pas"})
                continue

            soutenance['stage'] = stage.id

            try:
                soutenance_save = stage.soutenance.first()
                serializer = SoutenanceSerializer(soutenance_save, data=soutenance)
            except Soutenance.DoesNotExist:
                serializer = SoutenanceSerializer(data=soutenance)
                
            if serializer.is_valid() : 
                serializer.save()
                continue
            errors.append({"stage" : stage, "errors" : serializer.errors})

        if errors :
            return Response({"errors" : errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success" : "toutes les soutenances ont été créees avec succès"}, status= status.HTTP_201_CREATED)

class importSession(APIView):
    permission_classes = [IsAuthenticated, AdminPermission]
    def post(self, request, format = None):
        filiere = request.user.instance.filiere

        sessions_data = request.data

        errors = []
        for session in sessions_data :
            nom_session = session.get('nom')
            
            if not nom_session :
                errors.append({"session" : session, "errors" : "la session doit avoir un nom de sessione : nom  "})
                continue

            try : 
                Session.objects.get(nom= nom_session)
                errors.append({"session" : session, "errors" : "la session avec ce nom existe déjà"})
                continue
            except Session.DoesNotExist : 
                pass

            session['filiere'] = filiere.pk
            serializer = SessionSerializer(data=session)

            if serializer.is_valid():
                #serializer.save()
                continue
            errors.append({"session" : session, "errors" : serializer.errors})

        if errors :
            return Response({"errors" : errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success" : "toutes les sessions ont été créees avec succès"}, status= status.HTTP_201_CREATED)

class importJury(APIView):
    permission_classes = [IsAuthenticated, AdminPermission]

    def post (self, request, format = None):
        jurys_data = request.data
        filiere = request.user.instance.filiere

        errors = []
        for jury_all in jurys_data :
            jury_info = jury_all.copy()

            # on vérifie que toutes les données envoyé sont bien présentes
            jury = jury_all.pop('jury', None)
            if not jury :
                errors.append({"jury" : jury_info, "errors" : "vous n'avez pas spécifié les informations du jury"})
                continue
            
            nom_session = jury.pop('nom_session', None)
            if not nom_session :
                errors.append({"jury" : jury_info, "errors" : "le jury doit être associé à une session : nom_session"})
                continue

            membresJury = jury_all.pop('membresJury', None)
            if not membresJury :
                errors.append({"jury" : jury_info, "errors" : "vous devez spécifié les membres du jurys"})
                continue
            
            num_jury = jury.get('num_jury', None)
            if not num_jury :
                errors.append({"jury" : jury_info, "errors" : "le jury doit avoir un numéro de jury"})
                continue

            if len(membresJury) == 0 :
                errors.append({"jury" : jury_info, "errors" : "le jury doit contenir au moins un membre"})
                continue

            try :
                session = Session.objects.get(nom = nom_session, filiere = filiere)

            except Session.DoesNotExist:
                errors.append({"jury" : jury_info, "errors" : f"la session {nom_session} n'existe pas pour la filiere {filiere.nom}"})
                continue

            #on ajoute l'id de la session aux données de jury
            jury['session'] = session.id

            jury_save = None
            try :
                jury_save = Jury.objects.get(session = session, num_jury = num_jury)
                serializer = JuryImportSerializer(jury_save, data= jury)
            except Jury.DoesNotExist :
                serializer = JuryImportSerializer(jury)

            if serializer.is_valid():
                jury_save : Jury= serializer.save()
            else : 
                errors.append({"jury" : jury_all, "errors" : serializer.errors})
                continue

            jury_save.membreJury.clear()
            jury_save.save()

            for email in membresJury :
                errors_membresJury = []
                try :
                    membreJury = MembreJury.objects.get(email = email)
                except MembreJury.DoesNotExist :
                    errors_membresJury.append({"errors" : f"le membre jury avec l'adresse mail : {email} n'existe pas, il n'a pas été ajouté au jury"})
                    continue

                jury_save.membreJury.add(membreJury)

            if errors_membresJury :
                errors.append({"jury" : jury_info, "errors" : errors_membresJury})

        if errors :
            return Response({"errors" : errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success" : "toutes les sessions ont été créees avec succès"}, status= status.HTTP_201_CREATED)
