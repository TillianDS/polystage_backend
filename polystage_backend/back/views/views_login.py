from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser
from ..serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login, authenticate

class CostumLogin(APIView):
    """
    permet d'authentifier l'utilisateur et de la connecter à l'application

    type de requete : POST
    
    arguments requete :
    "email" : email de l'utilisateur
    "password" : nouveau mot de passe

    Response : 
    si les identifiants :
        - "id" : identifiants utilisateurs 
        - "token" : token d'authentification
        - "type utilisateur" : type de l'utilisateur qui se connecte

    """

    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        user = authenticate (request, email= email, password = password)
        if user :
            user2 = CustomUser.objects.get(email = email)
            if not user2.first_connection: 
                login(request, user2) 

                serializer = UserSerializer(user)
                token, create = Token.objects.get_or_create(user = user)
                return Response({'token' : token.key, 'user_id' : serializer.data["id"], 'profile' : serializer.data['profile']}, status=status.HTTP_202_ACCEPTED) 
            return Response({"first_connection" : True})
        return Response({'error' : "password or email are not correct"}, status=status.HTTP_401_UNAUTHORIZED)


class Checkemail (APIView) :
    def post (self, request, format = None) :
        return Response({"send" : True})




class Change_password (APIView) :
    def get_user (self, pk):
        return CustomUser.objects.get(pk = pk)
    
    def verify_passsword (self, password1, password2, request) :
        
        password_length = 7

        if password1 != password2:
            return {"error": "Les mots de passe ne correspondent pas"}
        if len(password1) < password_length:
            return {"error": f"Le mot de passe doit contenir au moins {password_length} caractères"}
        if not any(char.islower() for char in password1):
            return {"error": "Le mot de passe doit contenir au moins une lettre minuscule"}
        if not any(char.isupper() for char in password1):
            return {"error": "Le mot de passe doit contenir au moins une lettre majuscule"}
        if not any(char in r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]' for char in password1):
            return {"error": "Le mot de passe doit contenir au moins un caractère spécial"}
        
        return False
    """
    permet de changer le mot de passe dans le cadre d'un mot de passe oublié ou définition d'un nouveau mot de passe 

    type de requete : POST
    
    arguments requete :
    "password1" : nouveau mot de passe
    "password2" : vérification du mot de passe

    argument url : clé primaire de l'utilisateur concerné

    Response : l'utilisateur qui a été modifié

    """
    def post (self, request, pk, format = None) :
        user = self.get_user(pk)
        password1 = request.data["password1"]
        password2 = request.data["password2"]
        error = self.verify_passsword(password1, password2, request)

        if not (error == False) :
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(request.data['password1'])
        if user.first_connection :
            user.first_connection = False
            
        user.save()

        return Response(UserSerializer(user).data, status= status.HTTP_202_ACCEPTED)
    
