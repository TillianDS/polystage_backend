import random
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser, CodePassword
from ..serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from polystage_backend.permissions import *
from back.views.password import *
from mail.views import *
from datetime import datetime

def login_details (user):
    token, created = Token.objects.get_or_create(user=user)
    #login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
    serializer = UserSerializer(user)
    return Response({'user_id' : serializer.data["id"], "token" : token.key, 'profile' : serializer.data['profile']}, status=status.HTTP_202_ACCEPTED) 
             
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
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        user = authenticate (request, email= email, password = password, backend='django.contrib.auth.backends.ModelBackend',)        
        if user :
            if not user.first_connection:
                return login_details(user)
            return Response({"first_connection" : True})
        return Response({'error' : "password or email are not correct"}, status=status.HTTP_401_UNAUTHORIZED)
    
class Logout(APIView):
    def get(self, request):
        logout(request)
        return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)

"""
permet au superuser de se derogé à un utilisateur
"""
class derogationLogin (APIView):
    permission_classes = [IsAuthenticated, SuperUserPermission]

    def post (self, request):
        email = request.data['email']
        try :
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist :
            return Response({"error" : "l'adresse spécifié ne correspond à aucun utilisateur"})
        
        if not user.first_connection:
            return login_details(user)
        return Response({"first_connection" : True})

class SendCodeEmail (APIView) :
    permission_classes = [AllowAny]

    def generate_code(self, user): 
        code = random.randint(100000, 999999)

        code_data = {'code' : code, 'user' : user}
        try :
            codePassword_save = CodePassword.objects.get(user=user)
            serializer = CodePasswordSerializer(codePassword_save, data = code_data)
        except :
            serializer = CodePasswordSerializer(data = code_data)
        
        if not serializer.is_valid():
            return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return code
    
    """
    envoie un mail à l'utilisateur avec son code de réinitilisation, s'il existe
    si l'utilisateur n'existe pas, on a le même message de succès mais aucun mail n'est envoyé

    type de requete : POST
    
    arguments requete :
    "email" : email de l'utilisateur à réiniatiliser

    Response : 'success': 'email envoyé avec succès'

    """
    def post (self, request, format = None) :        
        try :
            email = request.data['email']
        except :
            return Response({'error': "vous devez préciser l'email de l'utilisateur"}, status=status.HTTP_400_BAD_REQUEST)

        try :   
            user = CustomUser.objects.get(email = email)
        except CustomUser.DoesNotExist :  
            return Response({'success': "mail envoyé avec succès si l'utilisateur existe et n'est pas un tuteur"}, status=status.HTTP_200_OK)
        
        if (user.profile == 'TUT') or (user.profile =='PRO') :
            return Response({'success': "mail envoyé avec succès si l'utilisateur existe et n'est pas un tuteur"}, status=status.HTTP_200_OK)

        code = self.generate_code()

        if isinstance(code, Response):
            return
        sendVerificationCode(send_mail = user.email, code=code) 
        return Response({'success': "mail envoyé avec succès si l'utilisateur existe et n'est pas un tuteur"}, status=status.HTTP_200_OK)
    
class verifyCode (APIView) :
    permission_classes = [AllowAny]

    def post (self, request, format = None) :
        try : 
            email = request.data['email']
            code = request.data['code']
        except :
            return Response({'error': "vous devez préciser un code et un email"}, status=status.HTTP_400_BAD_REQUEST)
        
        try :
            codePassword = CodePassword.objects.get(email = email, code = code, )
        except CodePassword.DoesNotExist: 
            return Response({'error': "il n'existe pas de codePassword pour l'email spécifié"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not codePassword.is_valid():
            return Response({'error': "le code n'est plus valide"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(True)
    
    
class ChangePassword (APIView) :
    permission_classes = [AllowAny]

    """
    permet de changer le mot de passe dans le cadre d'un mot de passe oublié ou définition d'un nouveau mot de passe 

    type de requete : POST
    
    arguments requete :
    "password1" : nouveau mot de passe
    "password2" : vérification du mot de passe

    argument url : clé primaire de l'utilisateur concerné

    Response : l'utilisateur qui a été modifié

    """
    def post (self, request, format = None) :
        try : 
            password1 = request.data["password1"]
            password2 = request.data["password2"]
        except :
            return Response({'error':'vous devez précisez password1 et password2'}, status=status.HTTP_400_BAD_REQUEST)
        
        try :
            email = request.data['email']
            code = request.data['code']
        except :
            return Response({'error':'vous devez précisez email et code'}, status=status.HTTP_400_BAD_REQUEST)

        verify = verify_passsword(password1, password2)

        if isinstance(verify, Response):
            return verify
        
        try :
            user = CustomUser.objects.get(email = email)
            codePassword = CodePassword.objects.get(email = user.email, code = code, )
        except : 
            return Response({'error': "il n'existe pas de codePassword pour l'email spécifié"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not codePassword.is_valid():
            return Response({'error': "le code n'est plus valide"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(request.data['password1'])
        if user.first_connection :
            user.first_connection = False
            
        user.save()

        return Response(UserSerializer(user).data, status= status.HTTP_202_ACCEPTED)

