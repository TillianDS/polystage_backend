
from rest_framework import serializers
from back.models import * 

#fichier de définition des différents serialiseurs pour chaque model

class FiliereSerializer (serializers.ModelSerializer) :
    class Meta :
        model = Filiere
        fields = ['id', 'nom', 'nom_directeur', 'prenom_directeur']

class PromoSerializer (serializers.ModelSerializer) :
    class Meta :
        model = Promo
        fields = ['id', 'annee', 'filiere']

class LoginSerializer(serializers.ModelSerializer) :
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta : 
        model = CustomUser
        fields = ['email', 'password']
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']

class EtudiantSerializer(UserSerializer):
    num_etudiant = serializers.CharField()
    date_naissance = serializers.DateField()

    class Meta:
        model = Etudiant
        fields = ['id', 'email', 'first_name', 'last_name', 'num_etudiant', 'date_naissance']

class TuteurSerializer (serializers.ModelSerializer) :
    class Meta : 
        model = Tuteur
        fields = ['id', 'email', 'first_name', 'last_name']

class EnseignantSerializer (serializers.ModelSerializer) :
    class Meta : 
        model = Enseignant
        fields = ['id', 'email', 'first_name', 'last_name']

class EntrepriseSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Entreprise
        fields = []

class StageSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Stage
        fields = ['id', 'confidentiel', 'sujet', 'date_debut', 'date_fin', 'entreprise', 'tuteur']

class JurySerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Jury
        fields = ['id', 'profesionnel', 'enseignant']

class SoutenanceSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Soutenance
        fields = ['id', 'date_soutenance', 'etudiant', 'jury', 'stage']