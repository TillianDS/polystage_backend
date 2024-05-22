
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

class PromoFiliereSerializer (serializers.ModelSerializer) :
    filiere = FiliereSerializer()
    class Meta :
        model = Promo
        fields = ['id', 'annee', 'filiere']
        
class UserSerializer(serializers.ModelSerializer):
    PROFILE_CHOICES = [
        ('ENS', 'Enseignant'),
        ('ETU', 'Etudiant'),
        ('ADM', 'Admin'),
        ('PRO', 'Professionnel'),
        ('TUT', 'Tuteur'),
    ]

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'first_connection', 'profile']

class EtudiantSerializer(UserSerializer):
    num_etudiant = serializers.CharField()
    date_naissance = serializers.DateField()
    profile = serializers.ChoiceField(choices=UserSerializer.PROFILE_CHOICES, default='ETU')

    class Meta:
        model = Etudiant
        fields = UserSerializer.Meta.fields + ['num_etudiant', 'date_naissance']

class TuteurSerializer (UserSerializer) :
    profile = serializers.ChoiceField(choices=UserSerializer.PROFILE_CHOICES, default='TUT')

    class Meta : 
        model = Tuteur
        fields = UserSerializer.Meta.fields

class EnseignantSerializer (UserSerializer) :
    profile = serializers.ChoiceField(choices=UserSerializer.PROFILE_CHOICES, default='ENS')

    class Meta : 
        model = Enseignant
        fields = UserSerializer.Meta.fields

class ProfessionnelSerializer (UserSerializer) :
    profile = serializers.ChoiceField(choices=UserSerializer.PROFILE_CHOICES, default='PRO')

    class Meta : 
        model = Professionnel
        fields = UserSerializer.Meta.fields

class AdminSerializer (UserSerializer) :
    profile = serializers.ChoiceField(choices=UserSerializer.PROFILE_CHOICES, default='ADM')

    class Meta : 
        model = Admin
        fields = UserSerializer.Meta.fields

class StageSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Stage
        fields = ['id', 'confidentiel', 'sujet', 'date_debut', 'date_fin', 'nom_entreprise', 'tuteur']

class JurySerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Jury
        fields = ['id', 'profesionnel', 'enseignant']

class SoutenanceSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Soutenance
        fields = ['id', 'date_soutenance', 'etudiant', 'jury', 'stage']