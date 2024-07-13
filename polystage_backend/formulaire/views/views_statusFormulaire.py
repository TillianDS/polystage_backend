from .views_list_details import *
from ..models import statusFormulaire
from ..serializers import StatusFormulaireSerializer
from rest_framework.response import Response


# définition des class pour la gestion des formulaires uniquement
class statutsFormulaireList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(statusFormulaire, StatusFormulaireSerializer)

class statusFormulaireDetails(Details):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attribute(statusFormulaire, StatusFormulaireSerializer, "statusFormulaire")

