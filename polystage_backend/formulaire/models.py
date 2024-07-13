from django.db import models

from back.models import Etudiant, Session, CustomUser, Stage

#gestion droits lectur ecriture
class Formulaire (models.Model):
    #id_createur
    id = models.CharField(max_length=200, primary_key=True)
    titre = models.TextField()
    description = models.CharField(max_length=400, blank= True, null= True)
    session =  models.ForeignKey(Session, on_delete=models.CASCADE)
    PROFILE_CHOICES = [
        ('TUT', 'Tuteur'),
        ('ETU', 'Etudiant'),
        ('JUR', 'Jury'),
    ]
    profile = models.CharField(max_length=3, choices=PROFILE_CHOICES)

    LANGUE_CHOICES = [
        ('FR', 'Français'),
        ('AN', 'Anglais'),
    ]
    langue = models.CharField(max_length=3, choices=LANGUE_CHOICES)
    
    
    def __str__ (self) :
        return str(self.title)

class Question (models.Model):
    titre = models.TextField()
    TYPE_CHOICES = [
        ('text', 'text'),
        ('paragraphe', 'paragraphe'),
        ('checkbox', 'checkbox'),
        ('dropdown', 'dropdown')
        ]
    type = models.CharField(max_length=15, choices = TYPE_CHOICES)
    obligatoire = models.BooleanField(default=True)
    formulaire = models.ForeignKey(Formulaire, related_name = 'question', on_delete=models.CASCADE)
    def __str__ (self) :
        return str(self.id) + " " +self.title
    
class ResponseForm (models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name = "stage")
    def __str__ (self) :
        return str(self.user) + " : " + str(self.content)

class CheckBox (models.Model):
    titre = models.CharField(max_length=200)
    question = models.ForeignKey(Question, related_name = 'checkbox', on_delete= models.CASCADE )
    content =models.BooleanField(default=False)
    def __str__ (self) :
        return str(self.question) + " " + str(self.title)

class ResponseCheckbox(models.Model):
    checkbox = models.ForeignKey(CheckBox, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    valeur = models.BooleanField(default=False)

class statusFormulaire(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    formulaire = models.ForeignKey(Formulaire, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('envoie', 'envoie'),
        ('sauvegarde', 'sauvegarde'),
        ('rendu', 'rendu'),
        ]
    statusForm = models.CharField(max_length=15, choices = STATUS_CHOICES, default= "envoie")

    class Meta:
        # Spécifie que la combinaison de 'nom' et 'filiere' doit être unique
        unique_together = ['formulaire', 'user']

    @property
    def is_rendu(self):
        if self.statusForm == 'rendu':
            return True
        return False