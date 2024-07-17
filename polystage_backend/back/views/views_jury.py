from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Jury, CustomUser, MembreJury, Filiere, Enseignant, Admin, Tuteur, Etudiant
from ..serializers import JurySerializer, JuryAffichageSerializer, MembreJurySerializer, JuryAllSerializer, JurysUserSerializer, EnseignantSerializer, EtudiantSerializer, UserSerializer, AdminSerializer, TuteurSerializer
from rest_framework.authentication import TokenAuthentication
from polystage_backend.permissions import *
from django.contrib.auth import get_user_model


class JuryList(APIView):
    def get (self, request, format = None):
        jury = Jury.objects.all()
        serializer = JuryAffichageSerializer(jury, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request, format = None):
        serializer = JurySerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JuryDetails (APIView):
    def getJury (self, pk):
        jury = Jury.objects.get(pk = pk)
        return jury
    
    def get (self, request, pk, format = None):
        jury = self.getJury(pk)
        serializer = JuryAffichageSerializer(jury)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put (self, request, pk, format = None):
        jury = self.getJury(pk)

        serializer = JurySerializer(jury, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        jury = self.getJury(pk)
        jury.delete()
        return Response({"success" : "jury supprimé avec succés"}, status = status.HTTP_200_OK)
    
"""
permet de savoir si un utilisateur fait partie d'un jury ou non
"""
class isJury(APIView):
    permission_classes = [JuryPermission]
    def post (self, request, format = None):
        try:
            id_user = request.data['id_user']
        except KeyError:
            return Response({"errors": "vous n'avez pas renseigné l'id de l'utilisateur"})
        
        try:
            user = MembreJury.objects.get(pk=id_user)
        except MembreJury.DoesNotExist:
            return Response({"is_jury": False, "jury": []})
        
        jury_id = []
        jurys = user.jury_set.all()

        for jury in jurys :
            jury_id.append(jury.id)
        return Response({"is_jury": True, 'jury' :jury_id})
    
class becomeLeader(APIView):
    permission_classes = [JuryPermission]

    def post(self, request, format = None):
        try:
            id_user = request.data['id_user']
        except KeyError:
            return Response({"errors": "vous n'avez pas renseigné l'id de l'utilisateur"})
        
        try:
            id_jury = request.data['id_jury']
        except KeyError:
            return Response({"errors": "vous n'avez pas renseigné l'id du jury"})
        
        try:
            jury = Jury.objects.get(pk=id_jury)
        except Jury.DoesNotExist:
            return Response({"errors": "le jury n'existe pas"})
        
        try:
            user = MembreJury.objects.get(pk = id_user)
        except MembreJury.DoesNotExist:
            return Response({"errors": "l'utilisateur n'est pas un membre de jury"})
        

        if user not in jury.membreJury.all() : 
            return Response({"errors": "l'utilisateur ne fait pas partie de ce jury"})
        
        jury.leader = user
        jury.save()
        return Response({'success' : "vous êtes maitenant le leader du jury"})
    
class isLeader(APIView):
    permission_classes = [JuryPermission]
    def post(self, request, format= None):
        id_membre = request.data.get('id_membreJury')
        id_jury = request.data.get('id_jury')

        if (not id_membre) | (not id_jury):
            return Response({'error' : "il manque l'id du membreJury ou du Jury"}, status=status.HTTP_400_BAD_REQUEST)
        
        try : 
            membreJury = MembreJury.objects.get(pk = id_membre)
        except MembreJury.DoesNotExist : 
            return Response({'error' : f"le membreJury {id_membre} n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)

        try : 
            jury = Jury.objects.get(pk = id_jury)
        except Jury.DoesNotExist : 
            return Response({'error' : f"le jury {id_jury} n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)


        #return Response(JurySerializer(jury).data)
        return Response ({'leader' : jury.leader == membreJury})

"""
retourne les soutenance liées à un jury
"""
class juryAll(APIView):
    permission_classes = [IsAuthenticated, AdminJuryPermission]
    def get(self,request, pk, format= None):        
        try : 
            jury = Jury.objects.get(pk=pk)
        except Jury.DoesNotExist:
            return Response({"error" :"le jury n'existe pas"})
    
        serializer = JuryAllSerializer(jury)

        return Response(serializer.data)
    
"""renvoie les jurys à l'utilisateur (membreJury) connecté"""
class getJuryMembreJury(APIView):
    permission_classes = [IsAuthenticated, JuryPermission]
    def get(self, request, format=None):
        serializer = JurySerializer(request.user.instance.jury_set, many = True)
        return Response(serializer.data)

"""
renvoie les jury relatifs à la filiere de l'administrateur connecté
"""
class getJury(APIView):
    permission_classes = [IsAuthenticated, AdminPermission]

    def get (self, request, format = None):
        filiere = request.user.instance.filiere
        jurys = Jury.objects.filter(filiere = filiere)
        serializer = JurySerializer(jurys, many = True)
        return Response(serializer.data)

"""
ajouter un membre jury à un jury, ou un jury au membreJury
"""    
class manageJuryMembreJury(APIView):
    permission_classes = [IsAuthenticated, AdminPermission]
    def post(self, request, format = None):
        try :
            id_membreJury = request.data['id_membreJury']
        except : 
            return Response({'error' : 'vous devez spécifier un membreJury : id_membreJury'})
        try :
            id_jury = request.data['id_jury']
        except :
            return Response({'error' : 'vous devez préciser un jury ; id_jury'})
        
        try :
            jury = Jury.objects.get(pk =id_jury)
        except Jury.DoesNotExist:
            return Response({'error' : f"le jury avec l'id {id_jury}"})
        
        try :
            membreJury = MembreJury.objects.get(pk=id_membreJury)
        except MembreJury.DoesNotExist:
            return Response({'error' : f"le membreJury avec l'id {id_membreJury}"})
        
        jury.membreJury.add(membreJury)
        jury.save()
        return Response({'success' : f'le membreJury  {id_membreJury} a été ajouté avec succès au jury {id_jury}'})
    
    def delete(self, request, format = None):
        try :
            id_membreJury = request.data['id_membreJury']
        except : 
            return Response({'error' : 'vous devez spécifier un membreJury : id_membreJury'})
        try :
            id_jury = request.data['id_jury']
        except :
            return Response({'error' : 'vous devez préciser un jury ; id_jury'})
        
        try :
            jury = Jury.objects.get(pk =id_jury)
        except Jury.DoesNotExist:
            return Response({'error' : f"le jury avec l'id {id_jury}"})
        
        try :
            membreJury = MembreJury.objects.get(pk=id_membreJury)
        except MembreJury.DoesNotExist:
            return Response({'error' : f"le membreJury avec l'id {id_membreJury}"})
        
        jury.membreJury.remove(membreJury)
        jury.save()
        return Response({'success' : f'le membreJury  {id_membreJury} a bien été dissocié du jury {id_jury}'})
    