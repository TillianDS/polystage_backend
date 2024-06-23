from rest_framework import serializers
from formulaire.models import *
from back.models import CustomUser

class FormulaireSerializer (serializers.ModelSerializer):
    class Meta :
        model = Formulaire
        fields = ['id', 'title', 'description', 'question']

    
class QuestionSerializer (serializers.ModelSerializer):
    formulaire = serializers.PrimaryKeyRelatedField(queryset=Formulaire.objects.all())
    class Meta :
        model = Question
        fields = ['id', 'title', 'type', 'formulaire']
        
class ResponseSerializer (serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = CustomUser.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset = Question.objects.all())
    class Meta :
        model = Response
        fields = ['id', 'content', 'question', 'user']

class CheckboxSerializer (serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset = Question.objects.all())
    class Meta :
        model = CheckBox
        fields = ['id', 'title', 'question']


# serializer pour l'affichage et l'enregistrement de tout un formulaire, question et checbox

class CheckboxAllSerializer (serializers.ModelSerializer):
    class Meta :
        model = CheckBox
        fields = ['id', 'title']

class QuestionAllSerializer (serializers.ModelSerializer):
    checkbox = CheckboxAllSerializer(many = True)
    class Meta :
        model = Question
        fields = ['id', 'title', 'type', 'checkbox']

class FormulaireAllSerializer (serializers.ModelSerializer):
    question = QuestionAllSerializer(many = True)

    class Meta :
        model = Formulaire
        fields = ['id', 'title', 'profile', 'description', 'question']
    
    def create(self, validated_data):
        question_data = validated_data.pop('question')
        formulaire = Formulaire.objects.create(**validated_data)
        for question in question_data:
            checkbox_data = question.pop('checkbox')
            question_create = Question.objects.create(formulaire=formulaire, **question)
            for checkbox in checkbox_data :
                CheckBox.objects.create(question = question_create, **checkbox)
        return formulaire
    
class FormulaireQuestionSerializer (serializers.ModelField):
    pass