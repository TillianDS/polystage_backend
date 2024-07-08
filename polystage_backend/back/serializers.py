from rest_framework import serializers
from back.models import * 

#fichier de définition des différents serialiseurs pour chaque model
class activeSerializer (serializers.ModelSerializer):
    is_active = serializers.BooleanField(default = True)
    class Meta :
        read_only_fields = ['is_active'] 

class FiliereSerializer (activeSerializer) :
    class Meta :
        model = Filiere
        fields = ['id', 'nom']

class SessionSerializer (activeSerializer) :
    class Meta :
        model = Session
        fields = ['id', 'nom', 'filiere']

class SessionFiliereSerializer(activeSerializer):
    sessions = serializers.SerializerMethodField()

    class Meta:
        model = Filiere
        fields = ['id', 'nom', 'sessions']

    def get_sessions(self, obj):
        sessions = Session.objects.filter(filiere=obj)
        return SessionSerializer(sessions, many=True).data
        
class UserSerializer(serializers.ModelSerializer):
    PROFILE_CHOICES = [
        ('ENS', 'Enseignant'),
        ('ETU', 'Etudiant'),
        ('ADM', 'Admin'),
        ('PRO', 'Professionnel'),
        ('TUT', 'Tuteur'),
    ]
    is_active = serializers.BooleanField(default = True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'first_connection', 'profile', 'is_active']
        read_only_fields = ['is_active']  

class EtudiantSerializer(UserSerializer):
    num_etudiant = serializers.CharField()
    profile = serializers.ChoiceField(choices=UserSerializer.PROFILE_CHOICES, default='ETU')
    sessions = serializers.PrimaryKeyRelatedField(queryset=Session.objects.all(), many=True, allow_empty=True)
    class Meta:
        model = Etudiant
        fields = UserSerializer.Meta.fields + ['num_etudiant', 'sessions']

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

class StageSerializer (activeSerializer) :
    tuteur = serializers.PrimaryKeyRelatedField(queryset = Tuteur.objects.all())
    class Meta : 
        model = Stage
        fields = "__all__"

class JurySerializer (activeSerializer) : 
    #leader = serializers.PrimaryKeyRelatedField(queryset = MembreJury.objects.all(), default = None)
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
    
class SoutenanceSerializer (activeSerializer) :
    date_soutenance = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y'], required=False, allow_null=True)
    heure_soutenance = serializers.TimeField(format= '%H:%M', input_formats=['%H:%M'], required=False, allow_null=True)

    class Meta : 
        model = Soutenance
        fields = "__all__"

class SoutenanceEtudiantSerializer (activeSerializer) :
    date_soutenance = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y'], required=False, allow_null=True)
    heure_soutenance = serializers.TimeField(format= '%H:%M', input_formats=['%H:%M'], required=False, allow_null=True)
    etudiant = EtudiantSerializer()
    class Meta : 
        model = Soutenance
        fields = "__all__"


# serializer d'importation
class StageAllSerializer (activeSerializer) :
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
    sessions = SessionFiliereSerializer(many = True)
    stage = serializers.SerializerMethodField()
    soutenance = serializers.SerializerMethodField()

    class Meta:
        model = Etudiant
        fields = UserSerializer.Meta.fields + ['num_etudiant', 'sessions', 'soutenance', 'stage']
    
    def get_soutenance(self, obj):
        soutenance = Soutenance.objects.filter(etudiant=obj)
        return SoutenanceSerializer(soutenance, many=True).data
    
    def get_stage(self, obj):
        stage = Stage.objects.filter(etudiant=obj)
        return StageAllSerializer(stage, many=True).data

class SessionEtudiantSerializer (activeSerializer):
    etudiants = serializers.SerializerMethodField()
    jurys = serializers.SerializerMethodField()

    class Meta :
        model = Session
        fields = ['id', 'nom', 'etudiants', 'jurys']

    def get_etudiants(self, obj):
        etudiants = Etudiant.objects.filter(sessions = obj)
        return EtudiantSerializer(etudiants, many= True).data
    
    def get_jurys (self, obj):
        session = Session.objects.get(pk=obj.pk)
        juries = Jury.objects.filter(
            soutenance__etudiant__sessions=session
        ).distinct()
        return JurySerializer(juries, many=True).data
