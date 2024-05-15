import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser, Enseignant, Tuteur, Admin, Professionnel, Etudiant
from ..serializers import UserSerializer, EnseignantSerializer, TuteurSerializer, ProfessionnelSerializer, AdminSerializer, EtudiantSerializer
from rest_framework.authentication import TokenAuthentication


"""
    méthode d'enregistrement pour chaque utilisateur
    verifie la correspondance des deux mots de passe et si les informations renvoyées sont les bonnes
    le mot de passe doit contenir une majusucle, une minuscule et un caractère spécial
    le mot de passe doit avoir une longueur minimum

    Response :
    information lié à l'utilisateur crée
"""
def enregistrement (request, serializer) :
    password_length = 7
    if serializer.is_valid(): 
        password1 = request.data["password1"]
        password2 = request.data["password2"]
        if password1 == password2 :
            if len(password1)>= password_length : 
                if re.findall('[a-z]', password1):
                    if re.findall('[A-Z]', password1):
                        if re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password1):
                            user = serializer.save()

                            user.set_password(request.data["password1"])
                            user.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return Response({"error": """le mot de passe doit cotenir un caractère spécial ()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?"""})
                    return Response({"error": "le mot de passe doit contentir une majuscule"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"error" : "le mot de passe doit contenir une minuscule"}, status=status.HTTP_400_BAD_REQUEST)
            return Response ({"error" : "le mot de passe doit faire plus de {} caractères".format(password_length)} , status=status.HTTP_400_BAD_REQUEST)
        return Response({"error" : "les mots de passes ne correspondent pas"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnseignantList(APIView):
    """
    définie les fonction sur l'enseignant
    """
    def get(self, request, format=None):
        enseignant = Enseignant.objects.all()
        serializer = EnseignantSerializer(enseignant, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = EnseignantSerializer(data = request.data)
        return enregistrement(request, serializer)

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

class User_details(APIView):
    """
    Retrieve, update or delete a User.
    """

    def get_User(self, pk) : 
        return CustomUser.objects.get(pk = pk)

    def get (self, request, pk, format = None) : 
        user = self.get_User(pk)
        serializer = UserSerializer(user)
        data = user.profile
        return Response(data)
    
    def put(self, request, pk, format = None):
        user = self.get_User(pk)
        serializer = UserSerializer(user,data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None) :
        user = self.get_User(pk)
        user.delete()
        return Response ({"success" : "utilisateur supprimé avec succès"}, status= status.HTTP_204_NO_CONTENT)
    