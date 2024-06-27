from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Etudiant, CustomUser, Tuteur, Stage, Soutenance, Jury
from formulaire.models import Question
from ..serializers import EtudiantSerializer, UserSerializer, StageSerializer, SoutenanceSerializer
from rest_framework.authentication import TokenAuthentication
from .views_users import UserList
from django.db.models import Q
from itertools import chain


class userSearchAllChamp (APIView):

    def get_string_data (self, request, data_name) :
        if data_name in request.data :
            data = request.data[data_name]
        else :
            data = ""
        return data
    """
    permet de rechercher des utilisateurs selon leur nom, prénom, email ou numéro étudiant
    la méthode recherche dans la base si les champs utilisateurs contiennent la chaine passé en data  
    le nom de l'utlisateur n'a pas besoin d'être complet et la reqeute ne tient pas compte de la casse
    la requete peut renvoyer un ou plusieurs utilisateurs

    type de requete : POST
    
    data requete : les données n'ont pas besoin d'être toutes présentes, si il y'en a aucune, selon renverra tous les utilisateurs
    "email" <string> : email de l'utilisateur
    "first_name" <string>: prenom
    "last_name" <string>: nom
    "date_naissance" <string>: data de naissance : format (day-month-year)
    "num_etudiant" <string> : numéro etudiant

    Response : informations correspondants à un utilisateurs
        - "id" <integer> : identifiant de l'utlisateur 
        - "email" <string> : email de l'utilisateur 
        - "first_name" <string>: prénom de l'utilisateur 
        - "last_name" <string>: nom de l'utilisateur
        - "first_connection" <Boolean>: l'utilisateur s'est il deja connecté 
        - "profile" <string>: profile" utilisateur

    """
    def post(self, request, format = None):
        prenom = self.get_string_data(request, 'first_name')
        nom = self.get_string_data(request, 'last_name')
        email = self.get_string_data(request, 'email')
        profile = self.get_string_data(request, 'profile')

        # seul l'etudiant possède une date de naissance ou un numéro etudiant
        if 'num_etudiant' in request.data:
            num_etudiant = self.get_string_data(request, 'num_etudiant')

            user = Etudiant.objects.filter(last_name__icontains = nom, first_name__icontains = prenom, num_etudiant = num_etudiant, email__icontains = email, profile = profile )

        else :
            user = CustomUser.objects.filter(last_name__icontains = nom, first_name__icontains = prenom, email__icontains = email)
        return Response(UserSerializer(user, many = True).data)

class userSearch (APIView):
    """
    permet de rechercher des utilisateurs selon leur nom, prénom, email ou numéro étudiant sur un seul champ
    la méthode recherche dans la base si les champs utilisateurs contiennent la chaine passé en data  
    le nom de l'utlisateur n'a pas besoin d'être complet et la reqeute ne tient pas compte de la casse
    la requete peut renvoyer un ou plusieurs utilisateurs

    type de requete : POST
    
    Response : informations correspondants à un utilisateurs

    """
    def post(self, request, format = None):
        search = request.data['search']

        etudiants = Etudiant.objects.filter(Q(last_name__icontains = search) |
                                           Q(first_name__icontains = search) | 
                                           Q(num_etudiant = search) | 
                                           Q(email__icontains = search))
        
        users = CustomUser.objects.filter(Q(email__icontains = search) | 
                                         Q(last_name__icontains = search) |
                                         Q(first_name__icontains = search))
        
        etudiants_data = EtudiantSerializer(etudiants, many = True).data
        users_data = (UserSerializer(users, many = True).data)

        users_results = list(chain(etudiants_data, users_data))

        return Response({'users' : users_results})

class stageSearch (APIView):

    """
    permet de rechercher des utilisateurs selon leur nom, prénom, email ou numéro étudiant sur un seul champ
    la méthode recherche dans la base si les champs utilisateurs contiennent la chaine passé en data  
    le nom de l'utlisateur n'a pas besoin d'être complet et la reqeute ne tient pas compte de la casse
    la requete peut renvoyer un ou plusieurs utilisateurs

    type de requete : POST
    
    Response : informations correspondants à un utilisateurs

    """
    def post(self, request, format = None):
        search = request.data['search']

        stages = Stage.objects.filter(Q(sujet__icontains = search) | #recherche selon le sujet
                                      Q(nom_entreprise__icontains =search) | #recherche selon le nom de l'entreprise
                                      Q(etudiant__num_etudiant__icontains = search) |#recherche selon le numéro étudiant
                                      Q(etudiant__email__icontains = search) #recherche selon le numéro étudiant
                                      ) 
        stages_data = StageSerializer(stages, many = True).data

        return Response({'stages' : stages_data})


class soutenanceSearch (APIView):
    """
    permet de rechercher des utilisateurs selon leur nom, prénom, email ou numéro étudiant sur un seul champ
    la méthode recherche dans la base si les champs utilisateurs contiennent la chaine passé en data  
    le nom de l'utlisateur n'a pas besoin d'être complet et la reqeute ne tient pas compte de la casse
    la requete peut renvoyer un ou plusieurs utilisateurs

    type de requete : POST
    
    Response : informations correspondants à un utilisateurs

    """
    def post(self, request, format = None):
        search = request.data['search']

        soutenances = Soutenance.objects.filter( Q(etudiant__num_etudiant__icontains = search) |#recherche selon le numéro étudiant
                                      Q(etudiant__email__icontains = search) |#recherche selon le numéro étudiant
                                      Q(etudiant__first_name__icontains = search) |
                                      Q(etudiant__last_name__icontains = search)
                                      ) 
        soutenances_data = SoutenanceSerializer(soutenances, many = True).data

        return Response({'soutenances' : soutenances_data})
    

class SetAllInactive(APIView):
    #rend inactive toutes les données active d'un model
    def modelInactive(self, models):
        models = models.objects.all()
        for model in models :
            model.delete()
    
    def post(self, request, format = None):
        self.modelInactive(Etudiant)
        self.modelInactive(Stage)
        self.modelInactive(Soutenance)
        self.modelInactive(Tuteur)
        self.modelInactive(Jury)
        self.modelInactive(Question)
        
        return Response ({"success" : "les données de Etudiants, Stage, Soutenances, Tuteur, Jury ont été rendus inactives" }, status=status.HTTP_200_OK)