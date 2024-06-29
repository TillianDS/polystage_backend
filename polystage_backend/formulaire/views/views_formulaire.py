from .views_list_details import *
from ..models import Formulaire, CheckBox, Question
from back.models import Etudiant
from ..serializers import FormulaireSerializer, CheckboxSerializer, FormulaireAllSerializer, QuestionSerializer
from rest_framework.response import Response
from django.db.models import Q

# définition des class pour la gestion des formulaires uniquement
class FormulaireList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Formulaire, FormulaireSerializer)

class FormulaireDetails(Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Formulaire, FormulaireSerializer, "Formulaire")


# définition des class pour la gestion des questions uniquement
class QuestionList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Question, QuestionSerializer)
        
class QuestionDetails (Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Question, QuestionSerializer, "Question")


# définition des class pour la gestion des checkbox uniquement
class CheckboxList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(CheckBox, CheckboxSerializer)

class CheckboxDetails(Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(CheckBox, CheckboxSerializer, "Checkbox")


# définition des class pour la création de formulaire, question et checkbox en même temps
class CreateFormulaireAll(APIView):
    def post(self, request, format= None):
        serializer = FormulaireAllSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetFormulaireAll(APIView):
    def get(self, request, pk, format= None):
        formulaire = Formulaire.objects.get(pk=pk)
        serializer = FormulaireAllSerializer(formulaire)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
permet de rechercher un formulaire selon son titre, sa description, le rôle à qui il s'adresse, sa filière
"""  
class FormulaireSearch (APIView):
    def post(self, request, format = None):
        search = request.data['search']

        formulaire = Formulaire.objects.filter(Q(titre__icontains = search) |
                                           Q(profile__icontains = search) | 
                                           Q(description__icontains = search) | 
                                           Q(filiere__nom__icontains = search))
        
        return Response(FormulaireSerializer(formulaire, many = True).data)

"""
retrouver le formulaire en fonction de l'étudiant pour qui il est rempli et du profile de l'utilisateur qui va le remplir
"""
class retrieveFormulaire (APIView):
    def post (self, request, format =None):
        id_etudiant = request.data["id_etudiant"]

        profile = request.data["profile"]
        filiere = Etudiant.objects.get(pk=id_etudiant).promo.filiere
        

        formulaire = filiere.formulaire_set.filter(profile=profile)

        return Response(FormulaireSerializer(formulaire, many = True).data)

