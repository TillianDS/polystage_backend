import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser, Enseignant, Tuteur, Admin, Professionnel, Etudiant
from ..serializers import UserSerializer, EnseignantSerializer, TuteurSerializer, ProfessionnelSerializer, AdminSerializer, EtudiantSerializer
from rest_framework.authentication import TokenAuthentication


class UserList(APIView):

    """
        méthode d'enregistrement pour chaque utilisateur
        verifie la correspondance des deux mots de passe et si les informations renvoyées sont les bonnes
        le mot de passe doit contenir une majusucle, une minuscule et un caractère spécial
        le mot de passe doit avoir une longueur minimum

        Response :
        information lié à l'utilisateur crée
    """
        

    def choice_serializer (self, profile, user, many) :
        if profile == 'ENS' : 
            return EnseignantSerializer(user, many = many)
        elif profile == 'ETU':
            return EtudiantSerializer(user, many = many)
        elif profile == 'ADM':
            return AdminSerializer(data = user, many = many)
        elif profile == 'PRO':
            return ProfessionnelSerializer(data = user, many= many)
        elif profile == 'TUT':
            return TuteurSerializer(data = user, many = many)
        
    def choice_user (self, profile):
        if profile == 'ENS' : 
            return Enseignant.objects.all()
        elif profile == 'ETU':
            return Etudiant.objects.all()
        elif profile == 'ADM':
            return Admin.objects.all()
        elif profile == 'PRO':
            return Professionnel.objects.all()
        elif profile == 'TUT':
            return Tuteur.objects.all()

    """
    définie les fonction sur l'enseignant
    """
    def get(self, request, profile, format=None):
        user = self.choice_user(profile)
        serializer = self.choice_serializer(profile, user, True)
        
        if serializer:
            return Response(serializer.data) 
        return Response({"error" : "le profile n'est pas valide"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, profile, format=None):
        serializer = self.choice_serializer(profile, request.data, False)
        
        password_length = 7
        if serializer.is_valid(): 
            password1 = request.data["password1"]
            password2 = request.data["password2"]

            if password1 != password2:
                return Response({"error": "Les mots de passe ne correspondent pas"}, status=status.HTTP_400_BAD_REQUEST)
            if len(password1) < password_length:
                return Response({"error": f"Le mot de passe doit contenir au moins {password_length} caractères"}, status=status.HTTP_400_BAD_REQUEST)
            if not any(char.islower() for char in password1):
                return Response({"error": "Le mot de passe doit contenir au moins une lettre minuscule"}, status=status.HTTP_400_BAD_REQUEST)
            if not any(char.isupper() for char in password1):
                return Response({"error": "Le mot de passe doit contenir au moins une lettre majuscule"}, status=status.HTTP_400_BAD_REQUEST)
            if not any(char in r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]' for char in password1):
                return Response({"error": "Le mot de passe doit contenir au moins un caractère spécial"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()

            user.set_password(password1)
            user.save()
            return Response(user, status=status.HTTP_201_CREATED)
                            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EtudiantList(APIView):
    
    def get(self, request, format=None):
        etudiant = Etudiant.objects.all()
        serializer = EtudiantSerializer(etudiant, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = EtudiantSerializer(data = request.data)
        return enregistrement(request, serializer)
    
class TuteurList(APIView):
    
    def get(self, request, format=None):
        tuteur = Tuteur.objects.all()
        serializer = TuteurSerializer(tuteur, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = TuteurSerializer(data = request.data)
        return enregistrement(request, serializer)
  
class ProfessionnelList(APIView):
    
    def get(self, request, format=None):
        professionnel = Professionnel.objects.all()
        serializer = ProfessionnelSerializer(professionnel, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = ProfessionnelSerializer(data = request.data)
        return enregistrement(request, serializer)

class AdminList(APIView):
    
    def get(self, request, format=None):
        admin = Admin.objects.all()
        serializer = AdminSerializer(admin, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = AdminSerializer(data = request.data)
        return enregistrement(request, serializer)

class UserDetails(APIView):
    """
    Retrieve, update or delete a User.
    """

    def get_User(self, pk) : 
        return CustomUser.objects.get(pk = pk)

    def get (self, request, pk, format = None) : 
        user = self.get_User(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk, format = None):
        user = self.get_User(pk)
        data = request.data.copy()

        data['profile'] =  user.profile
        serializer = UserSerializer(user,data = data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None) :
        user = self.get_User(pk)
        user.delete()
        return Response ({"success" : "utilisateur supprimé avec succès"}, status= status.HTTP_204_NO_CONTENT)
    