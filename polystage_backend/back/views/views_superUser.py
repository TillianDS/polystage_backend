from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import CustomUser
from ..serializers import UserSerializer
from rest_framework import status
from polystage_backend.permissions import *

class createSuperUser(APIView):
    
    def post (self, request, format= None) :
        email = request.data.get('email')
        firstName = request.data.get('first_name')
        lastName = request.data.get('last_name')

        if not email or not firstName or not lastName:
            return Response({"error": "Tous les champs sont obligatoires : email, first_name, last_name"}, status=status.HTTP_400_BAD_REQUEST)
    
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "L'adresse e-mail existe déjà."}, status=status.HTTP_400_BAD_REQUEST)
        
        try :
            password1 = request.data["password1"]
            password2 = request.data["password2"]
        except :
            return Response({'error' : "vous devez spécifier un mot de passe"})
        password_length = 7

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
            
        user = CustomUser.objects.create(
            email=email,
            is_staff=True,
            is_superuser=True,
            profile = 'SPR',
            first_name= firstName,
            last_name = lastName
        )
        user.set_password(password1)
        user.save()
        return Response(UserSerializer(user).data)
    
    def delete(slef, request, format = None):
        user = CustomUser.all_user.get(pk=66)
        user.hard_delete()
        return Response("delete")
    
class createAdmin(APIView):
    pass