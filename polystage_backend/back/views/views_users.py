from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser, Enseignant, Tuteur, Admin, Professionnel, Etudiant, Session
from ..serializers import UserSerializer, EnseignantSerializer, TuteurSerializer, ProfessionnelSerializer, AdminSerializer, EtudiantSerializer, SessionSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

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
            return AdminSerializer(user, many = many)
        elif profile == 'PRO':
            return ProfessionnelSerializer(user, many= many)
        elif profile == 'TUT':
            return TuteurSerializer(user, many = many)
        else :
            return 'error'
        
    def choice_deserializer (self, profile, user, many) :
        if profile == 'ENS' : 
            return EnseignantSerializer(data =user, many = many)
        elif profile == 'ETU':
            return EtudiantSerializer(data = user, many = many)
        elif profile == 'ADM':
            return AdminSerializer(data =user, many = many)
        elif profile == 'PRO':
            return ProfessionnelSerializer(data = user, many= many)
        elif profile == 'TUT':
            return TuteurSerializer(data = user, many = many)
        else :
            return 'error'
          
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
    def getSession(self, pk):
        return Session.objects.get(pk=pk)
    
    def get(self, request, format=None):
        profile = request.data['profile']
        user = self.choice_user(profile)
        
        if user != 'error':
            serializer = self.choice_serializer(profile, user, True)
            return Response(serializer.data) 
        return Response({"error" : "le profile n'est pas bon"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        data = request.data
        profile = data['profile']

        """
        if profile == 'ETU' :
            data = data.copy()
            data['sessions'] = Session.objects.get(pk=request.data['sessions']).pk
        """
        serializer = self.choice_deserializer(profile, data, False)
        
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
            
            #user = serializer.save()
            #user.set_password(password1)
            """
            if profile == 'ETU':
                user:Etudiant
                session = request.data.get('id_session')
                if session
                user.sessions = self.getSession(pk=session)
            user.save()
            """
            return Response(serializer.data, status=status.HTTP_201_CREATED)
                            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetails(APIView):
    """
    Retrieve, update or delete a User.
    """
    def choice_serializer (self, profile, user, many) :
        if profile == 'ENS' : 
            return EnseignantSerializer(user, many = many)
        elif profile == 'ETU':
            return EtudiantSerializer(user, many = many)
        elif profile == 'ADM':
            return AdminSerializer(user, many = many)
        elif profile == 'PRO':
            return ProfessionnelSerializer(user, many= many)
        elif profile == 'TUT':
            return TuteurSerializer(user, many = many)
        else :
            return 'error'
        
    def choice_deserializer (self, profile, user, data, many) :
        if profile == 'ENS' : 
            return EnseignantSerializer(user,data =data, many = many)
        elif profile == 'ETU':
            return EtudiantSerializer(user,data = data, many = many)
        elif profile == 'ADM':
            return AdminSerializer(user,data =data, many = many)
        elif profile == 'PRO':
            return ProfessionnelSerializer(user,data = data, many= many)
        elif profile == 'TUT':
            return TuteurSerializer(user, data = user, many = many)
        else :
            return 'error'
          
    def choice_user (self,pk, profile):
        if profile == 'ENS' : 
            return Enseignant.objects.get(pk=pk)
        elif profile == 'ETU':
            return Etudiant.objects.get(pk=pk)
        elif profile == 'ADM':
            return Admin.objects.get(pk=pk)
        elif profile == 'PRO':
            return Professionnel.objects.get(pk=pk)
        elif profile == 'TUT':
            return Tuteur.objects.get(pk=pk)
        
    def get_User(self, pk) : 
        return CustomUser.objects.get(pk = pk)

    def get (self, request, pk, format = None) : 
        profile = CustomUser.objects.get(pk=pk).profile
        user = self.choice_user(pk, profile)

        serializer = self.choice_serializer(profile, user, False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format = None):
        user = self.choice_user(pk, 'ETU')

        serializer = self.choice_deserializer('ETU', user, request.data, False)
        
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None) :
        user = self.get_User(pk)
        user.delete()
        return Response ({"success" : "utilisateur supprimé avec succès"}, status= status.HTTP_200_OK)

class UserAllList(APIView):
    def get(self, request, format=None):
        #profile = request.data['profile']
        user = Etudiant.all_user.all()
        
        serializer = EtudiantSerializer(user, many = True)
        return Response(serializer.data) 
        return Response({"error" : "le profile n'est pas bon"}, status=status.HTTP_400_BAD_REQUEST)
    
class SetMdp (APIView):
    def post (self, request, format = None):
        user = CustomUser.objects.get(email = request.data['email'])
        user.set_password(request.data['password'])
        user.save()