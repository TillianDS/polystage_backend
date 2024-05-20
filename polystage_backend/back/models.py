from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

#on définie ici une class pour les utilisateurs afin de pouvoir définir leur mail en tant que clé de connexion
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire.")
        email = self.normalize_email(email)
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

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CodePassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.IntegerField()

class Admin(CustomUser):
    
    class Meta : 
        verbose_name = 'Admin'

class Tuteur(CustomUser):
    class Meta : 
        verbose_name = 'Tuteur'

class Enseignant(CustomUser):
    class Meta : 
        verbose_name = 'Enseignant'

class Professionnel(CustomUser):
    class Meta : 
        verbose_name = 'Professionnel'

class Stage(models.Model):
    
    sujet = models.TextField()
    confidentiel = models.BooleanField(default= False)
    date_debut = models.DateField()
    date_fin = models.DateField()
    tuteur =  models.ForeignKey(Tuteur, on_delete=models.CASCADE )
    nom_entreprise = models.CharField(max_length= 200)

class Jury(models.Model):
    professionnel = models.ManyToManyField(Professionnel)
    enseignant = models.ManyToManyField(Enseignant)


class Filiere(models.Model):
    nom = models.CharField(max_length = 100, unique=True)
    nom_directeur = models.CharField(max_length = 100)
    prenom_directeur = models.CharField(max_length = 100)

    def __str__(self):
        return self.nom


class Promo(models.Model):
    annee = models.IntegerField(default = -1)
    filiere =  models.ForeignKey(Filiere, on_delete= models.CASCADE)

    def __str__(self):
        return self.filiere.nom + " " + str(self.annee)


class Etudiant (CustomUser):
    num_etudiant = models.CharField(max_length= 15)
    date_naissance = models.DateField()
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE )

    class Meta : 
        verbose_name = 'Etudiant'

class Soutenance(models.Model):
    date_soutenance = models.DateTimeField()
    heure_soutenance = models.TimeField(default = None)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE )
    jury =  models.ForeignKey(Jury, on_delete=models.CASCADE )
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE )


