from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *
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
            user.first
            if True : 
                login(request, user) 

                serializer = UserSerializer(user)
                token, create = Token.objects.get_or_create(user = user)
                return Response({'token' : token.key, 'user_id' : serializer.data["id"], 'type utilisateur' : serializer.data['profile']}, status=status.HTTP_202_ACCEPTED) 
            return Response({"first_connection" : True})
        return Response({'error' : "password or email are not correct"}, status=status.HTTP_401_UNAUTHORIZED)


class Checkemail (APIView) :
    def post (self, request, format = None) :
        return Response({"send" : True})




class Change_password (APIView) :
    
    def verify_set_passsword (request, user) :
        password1 = request.data["password1"]
        password2 = request.data["password2"]
        if password1 == password2 :
            user.set_password(password1)
            return True
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
        user = CustomUser.objects.get(pk = pk)
        

        if self.verify_set_passsword(request, user):
            if user.first_connection :
                user.first_connection = False
            
            user.save()

            return Response(UserSerializer(user).data, status= status.HTTP_202_ACCEPTED)
        return Response({"errors" : "les mots de passe ne sont aps identiques"}, status= status.HTTP_400_BAD_REQUEST)
    
