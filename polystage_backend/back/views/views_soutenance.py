from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Soutenance, CustomUser, MembreJury, Jury
from ..serializers import SoutenanceSerializer, JurySerializer
from rest_framework.authentication import TokenAuthentication
from .views_list_details import List, Details

class SoutenanceList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Soutenance, SoutenanceSerializer)

class SoutenanceDetails(Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Soutenance, SoutenanceSerializer, "Soutenance")

class setNote(APIView):
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
