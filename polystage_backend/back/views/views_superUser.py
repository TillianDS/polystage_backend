from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import CustomUser, Filiere, Admin
from ..serializers import UserSerializer, AdminSerializer
from rest_framework import status
from polystage_backend.permissions import *

def verifyPassword (request):
    password_length = 7

    try :
        password1 = request.data["password1"]
        password2 = request.data["password2"]
    except :
        return Response({'error' : "vous devez spécifier un mot de passe"})
    
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
    return password1

class superUserList(APIView):
    permission_classes = [SuperUserPermission]

    def get(self, request, format = None):
        admin = CustomUser.all_user.filter(profile = 'SPR')
        serializer = UserSerializer(admin, many = True)
        return serializer.data
    
    def post (self, request, format= None) :
        email = request.data.get('email')
        firstName = request.data.get('first_name')
        lastName = request.data.get('last_name')

        if not email or not firstName or not lastName:
            return Response({"error": "Tous les champs sont obligatoires : email, first_name, last_name"}, status=status.HTTP_400_BAD_REQUEST)
    
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "L'adresse e-mail existe déjà."}, status=status.HTTP_400_BAD_REQUEST)
        
        response = verifyPassword(request=request)
        
        if isinstance(response, Response):
            return response
        
        user = CustomUser.objects.create(
            email=email,
            is_staff=True,
            is_superuser=True,
            profile = 'SPR',
            first_name= firstName,
            last_name = lastName
        )
        user.set_password(response)
        user.save()
        return Response(UserSerializer(user).data)

class superUserDelete(APIView):
    permission_classes = [SuperUserPermission]

    def delete(self, pk, request, format = None):
        try : 
            user = CustomUser.all_user.get(pk=pk)
        except CustomUser.DoesNotExist :
            return Response({'error' : "l'utilisateur avec l'id : {pk}, n'existe pas"})
        user.hard_delete()
        return Response("super utilisateur supprimé avec succès")
    
class AdminList(APIView):
    permission_classes = [SuperUserPermission]

    def get(self, request, format = None):
        admin = Admin.objects.all()
        serializer = AdminSerializer(admin, many = True)
        return serializer.data
    
    def post (self, request, format = None) : 
        response = verifyPassword(request=request)

        if isinstance(response, Response):
            return response
        
        try :
            id_filiere = request.data['id_filiere']
            Filiere.object.get(pk = id_filiere)
        except Filiere.DoesNotExist : 
            return Response({"error" : "la filiere avec cet id n'existe pas"})
        
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        else : 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(response)
        user.save()
        return Response({'success' : "administrateur créer avec succès"})


class AdminDetails(APIView):

    def put(self, pk, request, format = None):
        try : 
            user = Admin.all_user.get(pk=pk)
        except Admin.DoesNotExist :
            return Response({'error' : "l'utilisateur avec l'id : {pk}, n'existe pas"})
        
        seriliazer = AdminSerializer(user, data = request.data)

        if seriliazer.is_valid():
            seriliazer.save()
            return Response({"sucess" : "administrateur créer avec succès"})
        return Response(seriliazer.errors)
        
    def delete(self, pk, request, format = None):
        try : 
            user = Admin.all_user.get(pk=pk)
        except Admin.DoesNotExist :
            return Response({'error' : "l'utilisateur avec l'id : {pk}, n'existe pas"})
        user.hard_delete()
        return Response({"sucess" : "super utilisateur supprimé avec succès"})
    
class SetPassword (APIView):
    permission_classes = [SuperUserPermission]
    def post (self, request, format = None):
        email = request.data['email']
        password = request.data['password']

        try : 
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist : 
            return Response({'error' : "l'utilisateur avec l'email : {email}, n'existe pas"})
        
        user.set_password(password)
        user.save()

        return Response()