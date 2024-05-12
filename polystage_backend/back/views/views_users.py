from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser, Etudiant, Enseignant, Tuteur, Admin, Professionnel
from ..serializers import UserSerializer, EtudiantSerializer, EnseignantSerializer
from rest_framework.authentication import TokenAuthentication


# Create your views here.   
class EnseignantList(APIView):
    
    def get(self, request, format=None):
        enseignant = Enseignant.objects.all()
        serializer = EnseignantSerializer(enseignant, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = EnseignantSerializer(data = request.data)
        if serializer.is_valid():
            enseignant = serializer.save()

            enseignant.set_password(request.data["password"])
            enseignant.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class User_details(APIView):
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
        serializer = UserSerializer(user,data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None) :
        user = self.get_User(pk)
        user.delete()
        return Response ({"success" : "utilisateur supprimé avec succès"}, status= status.HTTP_204_NO_CONTENT)
    
class Change_password (APIView) :
    """
    permet de changer le mot de passe dans le cadere d'un mot de passe oublié ou définition d'un nouveau mot de passe 

    type de requete : POST
    
    arguments requete :
    "password" : nouveau mot de passe

    argument url : clé primaire de l'utilisateur concerné

    Response : l'utilisateur qui a été modifié

    """
    def post (self, request, pk, format = None) :
        user = CustomUser.objects.get(pk = pk)
        password = request.data["password"]
        user.set_password(password)
        user.save()
        return Response(UserSerializer(user).data, status= status.HTTP_202_ACCEPTED )