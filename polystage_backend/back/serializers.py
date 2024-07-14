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
        fields = ['id', 'nom', 'filiere', 'is_active']

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
        ('SPR', 'Super User')
    ]
    is_active = serializers.BooleanField(default = True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'first_connection', 'profile', 'is_active']
        read_only_fields = ['is_active']  

class EtudiantSerializer(UserSerializer):
    profile = serializers.ChoiceField(choices=UserSerializer.PROFILE_CHOICES, default='ETU')
    class Meta:
        model = Etudiant
        fields = UserSerializer.Meta.fields + ['num_etudiant']

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
        fields = UserSerializer.Meta.fields + ['filiere']

class StageSerializer (activeSerializer) :
    date_debut = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y'])
    date_fin = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y'])

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


#  ----------------- serializer d'importation -----------------------------------
class StageAllSerializer (activeSerializer) :
    tuteur = TuteurSerializer()
    #soutenance = SoutenanceSerializer()
    class Meta : 
        model = Stage
        exclude = ['etudiant']

class JuryImportSerializer (activeSerializer) : 
    class Meta : 
        model = Jury
        exclude = ['membreJury']
# --------------- afficher toutes les informations de l'étudiant -----------------

class JuryEtudiantAllSeralizer(activeSerializer):
    jury = serializers.SerializerMethodField()
    class Meta : 
        model = Jury
        fields = '__all__' 
    def get_jury(self, obj):
        return SessionSerializer(obj.session).data
    
class SoutenanceEtudiantAllSeralizer(activeSerializer):
    jury = serializers.SerializerMethodField()
    class Meta : 
        model = Soutenance
        exclude = ['stage']

    def get_jury(self, obj):
        return JuryEtudiantAllSeralizer(obj.jury).data
    
class StageEtudiantAllSeralizer(activeSerializer):
    soutenance = serializers.SerializerMethodField()

    class Meta : 
        model = Stage
        exclude = ['etudiant']

    def get_soutenance(self, obj):
        soutenance = Soutenance.objects.filter(stage=obj)
        return SoutenanceEtudiantAllSeralizer(soutenance, many=True).data

class EtudiantAllSeralizer (UserSerializer) :
    stage = serializers.SerializerMethodField()

    class Meta:
        model = Etudiant
        fields = UserSerializer.Meta.fields + ['num_etudiant', 'stage']
    
    def get_stage(self, obj):
        stage = Stage.objects.filter(etudiant=obj)
        return StageEtudiantAllSeralizer(stage, many=True).data


# ----------------------- Affiche touts les informations de la sessions -----------------------------

class SessionAllSerializer (activeSerializer):
    etudiants = serializers.SerializerMethodField()
    jurys = serializers.SerializerMethodField()

    class Meta :
        model = Session
        fields = ['id', 'nom', 'etudiants', 'jurys']

    def get_etudiants(self, obj):
        soutenances = Soutenance.objects.filter(jury__session=obj)
        etudiants = Etudiant.objects.filter(stage__soutenance__in=soutenances)
        serializer = EtudiantSerializer(etudiants, many=True)
        return serializer.data
    
    def get_jurys (self, obj):
        return JurySerializer(obj.jury_set, many=True).data

# -------------------- affiche l'étudiant et la soutenance lié à un stage ---------------------

class StageTuteurSerializer (activeSerializer) :
    etudiant = EtudiantSerializer()
    soutenance = serializers.SerializerMethodField()
    class Meta : 
        model = Stage
        exclude = ['tuteur']

    def get_soutenance (self, obj):
        soutenance = Soutenance.objects.get(stage = obj)
        return SoutenanceEtudiantAllSeralizer(soutenance).data


# ------------- affiche les soutenances d'un jury ----------------y

class JuryEtudiantAllSeralizer(activeSerializer):
    jury = serializers.SerializerMethodField()
    class Meta : 
        model = Jury
        fields = '__all__' 
    def get_jury(self, obj):
        return SessionSerializer(obj.session).data
    
class StageJuryAllSeralizer(activeSerializer):
    etudiant = serializers.SerializerMethodField()
    class Meta : 
        model = Stage
        fields = '__all__'

    def get_etudiant(self, obj):
        etudiant = obj.etudiant
        return EtudiantSerializer(etudiant).data
    
class SoutenanceJuryAllSeralizer(activeSerializer):
    stage = serializers.SerializerMethodField()

    class Meta : 
        model = Soutenance
        exclude = ['jury']

    def get_stage(self, obj):
        stage = obj.stage
        return StageJuryAllSeralizer(stage).data

class JuryAllSerializer (UserSerializer) :
    soutenance = serializers.SerializerMethodField()

    class Meta:
        model = Jury
        fields = '__all__'

    def get_soutenance(self, obj):
        soutenance = Soutenance.objects.filter(jury=obj)
        return SoutenanceJuryAllSeralizer(soutenance, many=True).data

# ----------------- renvoie les jurys et leur sessions ----------------------

class JurysUserSerializer (UserSerializer) :
    session = SessionSerializer()

    class Meta:
        model = Jury
        fields = '__all__'


# -------------- renvoie les stage et etudiant encadré par le tuteur --------------------------

class StageTuteurSerializer (activeSerializer) :
    etudiant = EtudiantSerializer()

    class Meta:
        model = Stage
        exclude = ['tuteur']
