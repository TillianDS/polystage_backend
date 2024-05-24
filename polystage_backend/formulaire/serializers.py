from rest_framework import serializers
from formulaire.models import *

class FormulaireSerializer (serializers.ModelSerializer):
    class Meta :
        model = Formulaire
        fields = ['id', 'id', 'title', 'description']

    
class QuestionSerializer (serializers.ModelSerializer):
    formulaire = serializers.PrimaryKeyRelatedField(queryset=Formulaire.objects.all())
    class Meta :
        model = Question
        fields = ['id', 'title', 'type', 'formulaire']
        
class ResponseSerializer (serializers.ModelSerializer):
    class Meta :
        model = Response
        fields = ['id', 'question', 'user']

class ResponseSerializer (serializers.ModelSerializer):
    class Meta :
        model = CheckBox
        fields = ['id', 'title', 'question']
