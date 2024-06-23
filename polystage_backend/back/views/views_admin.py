from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Etudiant, CustomUser, Tuteur, Stage, Soutenance, Jury
from formulaire.models import Question
from ..serializers import EtudiantSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from .views_users import UserList


class GetUser (APIView):

    def get_string_data (self, request, data_name) :
        if data_name in request.data :
            data = request.data[data_name]
        else :
            data = ""
        return data
    """
    permet de rechercher des utilisateurs selon leur nom, prénom, data de naissance, email ou numéro étudiant
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
        if 'date_naissance' in request.data  or 'num_etudiant' in request.data:
            num_etudiant = self.get_string_data(request, 'num_etudiant')

            if 'date_naissance' in request.data :
                date_naissance_str = request.data['date_naissance']
                date_naissance = datetime.strptime(date_naissance_str, '%d-%m-%Y').date()
                user = Etudiant.objects.filter(last_name__icontains = nom, first_name__icontains = prenom, date_naissance = date_naissance, num_etudiant__icontains = num_etudiant, email__icontains = email)

            else :
                user = Etudiant.objects.filter(last_name__icontains = nom, first_name__icontains = prenom, num_etudiant = num_etudiant, email__icontains = email, profile = profile )

        else :
            user = CustomUser.objects.filter(last_name__icontains = nom, first_name__icontains = prenom, email__icontains = email)
        return Response(UserSerializer(user, many = True).data)

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