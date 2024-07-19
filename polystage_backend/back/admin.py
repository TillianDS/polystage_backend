from django.contrib import admin
from .models import *

# Définir une classe d'administration pour chaque modèle enfant

class SessionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Remplacez `active_users` par le manager de votre choix
        return Session.all_objects.get_queryset()

class SoutenanceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Remplacez `active_users` par le manager de votre choix
        return Soutenance.all_objects.get_queryset()
    def delete_model(self, request, obj):
        """
        Perform a soft delete or hard delete on the object.
        """
        # Pour une suppression douce
        obj.hard_delete()
    
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Stage)
admin.site.register(Admin)
admin.site.register(Tuteur)
admin.site.register(Enseignant)
admin.site.register(Professionnel)
admin.site.register(Jury)
admin.site.register(Filiere)
admin.site.register(Session, SessionAdmin)
admin.site.register(Etudiant)
admin.site.register(Soutenance, SoutenanceAdmin)
admin.site.register(CodePassword)