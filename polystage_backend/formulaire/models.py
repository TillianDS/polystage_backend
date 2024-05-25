from django.db import models

from back.models import CustomUser
# Create your models here.

#gestion droits lectur ecriture
class Formulaire (models.Model):
    #id_createur
    id = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank= True, null= True)
    def __str__ (self) :
        return str(self.title)

class Question (models.Model):
    title = models.CharField(max_length=200)
    TYPE_CHOICES = [
        ('text', 'text'),
        ('paragraphe', 'paragraphe'),
        ('checkbox', 'checkbox'),
        ('dropdown', 'dropdown')
        ]
    type = models.CharField(max_length=15, choices = TYPE_CHOICES)
    formulaire = models.ForeignKey(Formulaire, related_name = 'question', on_delete=models.CASCADE)
    def __str__ (self) :
        return str(self.id) + " " +self.title
    
class Response (models.Model):
    content = models.CharField(max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __str__ (self) :
        return str(self.user) + " : " + str(self.content)

class CheckBox (models.Model):
    title = models.CharField(max_length=200)
    question = models.ForeignKey(Question, related_name = 'checkbox', on_delete= models.CASCADE )
    def __str__ (self) :
        return str(self.question) + " " + str(self.title)
