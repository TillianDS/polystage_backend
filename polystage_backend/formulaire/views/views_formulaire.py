from .views_list_details import *
from ..models import Formulaire, CheckBox, Question
from ..serializers import FormulaireSerializer, CheckboxSerializer, FormulaireAllSerializer, QuestionSerializer

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
class FormulaireAllList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Formulaire, FormulaireAllSerializer)

class FormulaireAllDetails(Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(Formulaire, FormulaireAllSerializer, "Formulaire")

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
