
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
    filiere = FiliereSerializer(read_only = True)
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
    profile = serializers.ChoiceField(choices=UserSerializer.PROFILE_CHOICES, default='ETU')
    promo = serializers.PrimaryKeyRelatedField(queryset = Promo.objects.all())

    class Meta:
        model = Etudiant
        fields = UserSerializer.Meta.fields + ['num_etudiant', 'promo']

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
    tuteur = serializers.PrimaryKeyRelatedField(queryset = Tuteur.objects.all())
    class Meta : 
        model = Stage
        fields = "__all__"

class JurySerializer (serializers.ModelSerializer) : 
    #membr = serializers.PrimaryKeyRelatedField(queryset=Professionnel.objects.all(), many=True)
    
    class Meta : 
        model = Jury
        fields = "__all__"
        
    """
    def create(self, validated_data):
        pro_data = validated_data.pop('professionnel')
        enseignant_data = validated_data.pop('enseignant')
        jury = Jury.objects.create(**validated_data)

        for pro in pro_data:
            professionnel = Professionnel.objects.get(id = pro.id)
            jury.professionnel.add(professionnel)

        for ens in enseignant_data :
            enseignant = Enseignant.objects.get(id = ens)
            jury.enseignant.add(enseignant)
            
        return jury
    """
class MembreJurySerializer (UserSerializer):
    class Meta: 
        model = MembreJury
        fields = UserSerializer.Meta.fields

class JuryAffichageSerializer (serializers.ModelSerializer) : 
    membreJury = MembreJurySerializer(MembreJury.objects.all(), many = True)
    class Meta : 
        model = Jury
        fields = "__all__"
    
class SoutenanceSerializer (serializers.ModelSerializer) :
    date_soutenance = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y'], required=False, allow_null=True)
    heure_soutenance = serializers.TimeField(format= '%H:%M', input_formats=['%H:%M'], required=False, allow_null=True)

    class Meta : 
        model = Soutenance
        fields = "__all__"


class FileSerializer (serializers.ModelSerializer):
    file = serializers.FileField(use_url=False)


# serializer d'importation
class StageAllSerializer (serializers.ModelSerializer) :
    tuteur = TuteurSerializer()
    class Meta : 
        model = Stage
        exclude = ['etudiant']

"""class SoutenanceAllSerializer (serializers.ModelSerializer) :
    etudiant = serializers.PrimaryKeyRelatedField(queryset = Etudiant.objects.all())
    jury = serializers.PrimaryKeyRelatedField(queryset = Jury.objects.all())
    date_soutenance = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y'])
    heure_soutenance = serializers.TimeField(format= '%H:%M', input_formats=['%H:%M'])
    class Meta : 
        model = Soutenance
        fields = "__all__"
        """

class EtudiantAllSeralizer (UserSerializer) :
    num_etudiant = serializers.CharField()
    promo = PromoFiliereSerializer()
    stage = StageAllSerializer(many =True)
    soutenance = SoutenanceSerializer(many = True)

    class Meta:
        model = Etudiant
        fields = UserSerializer.Meta.fields + ['num_etudiant', 'promo', 'stage', 'soutenance']

