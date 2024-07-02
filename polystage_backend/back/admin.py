from django.contrib import admin
from .models import *

# Définir une classe d'administration pour chaque modèle enfant


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Stage)
admin.site.register(Admin)
admin.site.register(Tuteur)
admin.site.register(Enseignant)
admin.site.register(Professionnel)
admin.site.register(Jury)
admin.site.register(Filiere)
admin.site.register(Session)
admin.site.register(Etudiant)
admin.site.register(Soutenance)
admin.site.register(CodePassword)