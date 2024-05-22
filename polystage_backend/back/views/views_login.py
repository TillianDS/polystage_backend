import random
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser, CodePassword
from ..serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings

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

class ChangePassword (APIView) :
    def get_user (self, pk):
        return CustomUser.objects.get(pk = pk)
    """
    vérifie la validité du mdp
    """
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

class gestionCode(APIView):
    def generate_code(self, user: CustomUser): 
        codePassword = CodePassword.objects.filter(user=user)
        code = random.randint(100000, 999999)

        if codePassword :
            codePassword = CodePassword.objects.get(user=user)
            codePassword.code = code
        else :
            codePassword = CodePassword.objects.create(user = user, code = code)
        codePassword.save()
        return code
 
    
    def get(self, request) :
        user = CustomUser.objects.get(email = 'tdhume@laposte.net')
        return Response({'code': self.generate_code(user)})
    
class SendCodeEmail (APIView) :
    """
    créer un nombre de manière aléatoire à 6 chiffre, permet de généré la code reset du mdp
    """
    def generate_code(self): 
        return random.randint(100000, 999999)
    
    """
    envoie un mail à l'utilisateur avec son code de réinitilisation, s'il existe
    si l'utilisateur n'existe pas, on a le même message de succès mais aucun mail n'est envoyé

    type de requete : POST
    
    arguments requete :
    "email" : email de l'utilisateur à réiniatiliser

    Response : 'success': 'email envoyé avec succès'

    """
    def post (self, request, format = None) :
        data = request.data
        if 'email' in data :
            to_email = data['email']

            user = CustomUser.objects.filter(email = to_email)
            
            if user :
                code = gestionCode.generate_code(user=user)
                subject = 'Réinitialiser votre mot de passe'
                message = 'Votre code de réinitialisation est le suivant %d'%(code)
                from_email = settings.EMAIL_HOST_USER
                send_mail(subject, message, from_email, [to_email])

            return Response({'success': 'email envoyé avec succès'}, status=status.HTTP_200_OK)
        return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    
class CheckCode (APIView) :
    def post (self, request, format = None) :
        email = request.data['email']
        code = request.data['code']

        codePassword : CodePassword = CodePassword.objects.get(email = email)
        codeBase = codePassword.code

        if (code != codePassword) :
            return Response({"success" : True})
        return Response({"success" : True})