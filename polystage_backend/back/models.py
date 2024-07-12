from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MaxValueValidator

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire.")
        email = self.normalize_email(email)

        try :
            user : CustomUser = self.get(email =email)
            user.is_active = True
            
        except CustomUser.DoesNotExist :
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
        
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    

class ActiveManager(CustomUserManager):
    def get_queryset(self):
        # Ne renvoie que les utilisateurs actifs
        return super().get_queryset().filter(is_active=True)
  
class CustomUser(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)

    first_connection = models.BooleanField(default= True)
    PROFILE_CHOICES = [
        ('ENS', 'Enseignant'),
        ('ETU', 'Etudiant'),
        ('ADM', 'Admin'),
        ('PRO', 'Professionnel'),
        ('TUT', 'Tuteur'),
    ]
    profile = models.CharField(max_length=3, choices=PROFILE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ActiveManager()
    all_user = CustomUserManager()

    class Meta : 
        indexes = [
            models.Index(fields=['email']),
        ]

    def delete(self):
        self.is_active = False
        self.save()

    def hard_delete(self, *args, **kwargs):
        super(CustomUser, self).delete(*args, **kwargs)

    def __str__(self):
        return self.email

    def verify_stage(self, id_stage):
        if self.profile == 'ETU':
            return self.stage.filter(pk=id_stage).exists()  # Assurez-vous que le related_name est 'stages' pour Etudiant
        elif self.profile == 'TUT':
            return self.stage_set.filter(pk=id_stage).exists()  # Assurez-vous que le related_name est correct pour Tuteur
        return True
    
class ActiveModel(models.Model):
    is_active = models.BooleanField(default=True)

    objects = ActiveManager() 
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def hard_delete(self, *args, **kwargs):
        super(ActiveModel, self).delete(*args, **kwargs)

class CodePassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.IntegerField()

class Admin(CustomUser):
    class Meta : 
        verbose_name = 'Admin'

class Tuteur(CustomUser):
    class Meta : 
        verbose_name = 'Tuteur'

class MembreJury(CustomUser):
    pass

class Enseignant(MembreJury):
    class Meta : 
        verbose_name = 'Enseignant'

class Professionnel(MembreJury):
    class Meta : 
        verbose_name = 'Professionnel'

class Filiere(ActiveModel):
    nom = models.CharField(max_length = 100, unique=True)

    def __str__(self):
        return self.nom

class Session(ActiveModel):
    nom = models.CharField(max_length=100)
    filiere =  models.ForeignKey(Filiere, on_delete= models.CASCADE)

    def __str__(self):
        return self.nom

class Jury(ActiveModel):
    membreJury = models.ManyToManyField(MembreJury)
    salle = models.CharField(max_length=100, null = True)
    batiment = models.CharField(max_length=100, null = True)
    campus = models.CharField(max_length=200, null = True)
    zoom = models.CharField(max_length=300, null = True )
    #models.models.URLField(_(""), max_length=200)
    num_jury = models.IntegerField()
    leader = models.ForeignKey(MembreJury, on_delete=models.CASCADE, related_name='leader', default=None, null= True)
    session =  models.ForeignKey(Session, on_delete=models.CASCADE)

class Etudiant (CustomUser):
    num_etudiant = models.CharField(max_length= 20, unique= True)

    class Meta : 
        verbose_name = 'Etudiant'
        indexes = [
            models.Index(fields=['num_etudiant']),
        ]

class Stage(ActiveModel):
    sujet = models.TextField()
    confidentiel = models.BooleanField(default= False)
    date_debut = models.DateField()
    date_fin = models.DateField()
    tuteur =  models.ForeignKey(Tuteur, on_delete=models.CASCADE)
    nom_entreprise = models.CharField(max_length= 400)
    etudiant = models.ForeignKey(Etudiant, related_name ='stage', on_delete=models.CASCADE )
    soutenu = models.BooleanField(default=False)

    def __str__(self):
        return self.sujet
    
    @property
    def StageSession(self):
        soutenances = self.soutenance_set
        if not soutenances:
            return None
        soutenance = soutenances.first()
        session = soutenance.jury.session if soutenance.jury else None
        return session

class Soutenance(ActiveModel):
    date_soutenance = models.DateField(blank= True, null = True)
    heure_soutenance = models.TimeField(blank = True, null = True)
    jury =  models.ForeignKey(Jury, on_delete=models.CASCADE, null= True )
    note = models.FloatField(validators=[MaxValueValidator(20.0)], null = True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE )
    soutenu = models.BooleanField(default=False)
