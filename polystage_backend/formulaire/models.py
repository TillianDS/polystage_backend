from django.db import models

from back.models import Etudiant, Filiere

#gestion droits lectur ecriture
class Formulaire (models.Model):
    #id_createur
    id = models.CharField(max_length=200, primary_key=True)
    titre = models.CharField(max_length=200)
    description = models.CharField(max_length=400, blank= True, null= True)
    filiere =  models.ForeignKey(Filiere, on_delete=models.CASCADE)
    PROFILE_CHOICES = [
        ('ENS', 'Enseignant'),
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
    titre = models.CharField(max_length=200)
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
    content = models.CharField(max_length=1000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name = "etudiant")
    def __str__ (self) :
        return str(self.user) + " : " + str(self.content)

class CheckBox (models.Model):
    titre = models.CharField(max_length=200)
    question = models.ForeignKey(Question, related_name = 'checkbox', on_delete= models.CASCADE )
    def __str__ (self) :
        return str(self.question) + " " + str(self.title)

class ResponseCheckbox(models.Model):
    checkbox = models.ForeignKey(CheckBox, on_delete=models.CASCADE)
    id_etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
