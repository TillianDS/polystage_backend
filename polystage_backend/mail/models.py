from django.db import models

# Create your models here.

class Mail (models.Model):
    sujet = models.CharField(max_length=400)
    contenu = models.CharField(max_length=2000)
    is_active = models.BooleanField()
    