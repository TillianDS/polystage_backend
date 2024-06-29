from .views_list_details import *
from ..models import Formulaire, CheckBox, Question
from back.models import Etudiant
from ..serializers import FormulaireSerializer, CheckboxSerializer, FormulaireAllSerializer, QuestionSerializer
from rest_framework.response import Response

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
    
class SearchFormulaire (APIView):
    def get_string_data (self, request, data_name) :
            if data_name in request.data :
                data = request.data[data_name]
            else :
                data = ""
            return data
    
    def post(self, request, format = None):
        titre = self.get_string_data(request, 'titre')
        description = self.get_string_data(request, 'description')
        profile = self.get_string_data(request, 'profile')

        #promo = 
        #filiere = 
        
        formulaire = Formulaire.objects.filter(titre__icontains = titre, description__icontains = description, profile__icontains = profile)
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

