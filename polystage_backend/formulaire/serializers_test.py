from rest_framework import serializers
from formulaire.models import *
from back.models import CustomUser


class CheckboxSerializer (serializers.ModelSerializer):
    class Meta :
        model = CheckBox
        fields = ['id', 'titre']

class QuestionSerializer (serializers.ModelSerializer):
    checkbox = CheckboxSerializer(many = True)
    class Meta :
        model = Question
        fields = ['id', 'titre', 'type', 'checkbox']

class FormulaireSerializer (serializers.ModelSerializer):
    question = QuestionSerializer(many = True)

    class Meta :
        model = Formulaire
        fields = ['id', 'titre', 'description', 'profile', 'question']
    
    def create(self, validated_data):
        question_data = validated_data.pop('question')
        formulaire = Formulaire.objects.create(**validated_data)
        for question in question_data:
            checkbox_data = question.pop('checkbox')
            question_create = Question.objects.create(formulaire=formulaire, **question)
            for checkbox in checkbox_data :
                CheckBox.objects.create(question = question_create, **checkbox)
        return formulaire

class ResponseSerializer (serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = CustomUser.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset = Question.objects.all())
    class Meta :
        model = Response
        fields = ['id', 'content', 'question', 'user']

