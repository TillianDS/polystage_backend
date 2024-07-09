from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Soutenance, CustomUser, MembreJury, Jury, Etudiant, Tuteur
from ..serializers import SoutenanceSerializer, JurySerializer
from rest_framework.authentication import TokenAuthentication
from .views_list_details import List, Details
from polystage_backend.permissions import *

class SoutenanceList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Soutenance, SoutenanceSerializer)

class SoutenanceDetails(Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Soutenance, SoutenanceSerializer, "Soutenance")

class setNote(APIView):
    permission_classes = [AdminJuryPermission]
    def post(self, request, format = None):
        id_user = request.data['id_user']
        id_soutenance = request.data['id_soutenance']
        id_jury = request.data['id_jury']
        
        note_str = request.data.get('note')

        if note_str is None:
            return Response({"errors": "La note est requise."}, status=400)

        # Convertir la virgule en point pour les nombres
        if isinstance(note_str, str):
            note_str = note_str.replace(',', '.')

        try:
            note = float(note_str)  # Convertir la chaîne en nombre flottant
        except ValueError:
            return Response({"errors": "La note doit être un nombre valide."})
        
        
        # Vérifier que la note est comprise entre 0 et 20
        if not (0 <= note <= 20):
            return Response({"errors": "La note doit être comprise entre 0 et 20."}, status=status.HTTP_400_BAD_REQUEST)
 
        user = CustomUser.objects.get(pk=id_user)

        if (user.profile == 'ENS') | (user.profile == 'PRO'):
            jury = Jury.objects.get(pk = id_jury)
            user = MembreJury.objects.get(pk=id_user)

            if jury.leader != user :
                return Response({'error' :"vous n'êtes pas leader du jury"})
        
        else :
            return Response({'error' :"vous n'êtes pas autorisé"})

        soutenance = Soutenance.objects.get(pk=id_soutenance)
        soutenance.note= note
        soutenance.save()
        return Response({'success' :"la note a bien été enregistré"})

"""
retourne les soutenance liées à un jury
"""
class getSoutenanceJury(APIView):
    def post(self,request, format= None):

        id_jury = request.data.get('id_jury')
        if not id_jury :
            return Response ({'error': "vous devez spécifier l'id du jury"}, status=status.HTTP_400_BAD_REQUEST)
        try : 
            jury = Jury.objects.get(pk=id_jury)
        except Jury.DoesNotExist:
            return Response({"error" :"le jury n'existe pas"})
        soutenance = jury.soutenance_set.all()
    
        serializer = SoutenanceEtudiantSerializer(soutenance, many = True)

        return Response(serializer.data)
    
class getSoutenanceTuteur(APIView):
    permission_classes = [TuteurPermission]

    def get (self, request, format = None):
        user = Tuteur.objects.get(pk= request.user.pk)
        serializer = SoutenanceSerializer(user.soutenance_set, many = True)

        return Response(serializer.data)