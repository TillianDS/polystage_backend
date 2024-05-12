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
    connecte l'utilisateur et renvoie un token d'authentification nécessaire 
    """
    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        user = authenticate (request, email= email, password = password)
        if user :
            serializer = UserSerializer(user)
            token, create = Token.objects.get_or_create(user = user)
            model_name = user._meta.model.__name__
            return Response({'token' : token.key, 'user_id' : serializer.data["id"], 'type utilisateur' : model_name}, status=status.HTTP_202_ACCEPTED) 
        return Response({'error' : "password or email are not correct"}, status=status.HTTP_401_UNAUTHORIZED)
