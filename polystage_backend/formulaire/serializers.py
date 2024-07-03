from rest_framework import serializers
from formulaire.models import *
from back.models import CustomUser

class FormulaireSerializer (serializers.ModelSerializer):
    class Meta :
        model = Formulaire
        fields = "__all__"


class QuestionSerializer (serializers.ModelSerializer):
    formulaire = serializers.PrimaryKeyRelatedField(queryset=Formulaire.objects.all())
    class Meta :
        model = Question
        fields = "__all__" 

class ResponseCheckboxSerializer (serializers.ModelSerializer):
    class Meta:
        model = ResponseCheckbox
        fields = ['id', 'id_etudiant', 'checkbox', 'valeur']
        
class ResponseSerializer (serializers.ModelSerializer):
    id_etudiant = serializers.PrimaryKeyRelatedField(queryset = Etudiant.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset = Question.objects.all())
    class Meta :
        model = ResponseForm
        fields = "__all__"

class CheckboxSerializer (serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset = Question.objects.all())
    class Meta :
        model = CheckBox
        fields = ['id', 'titre', 'question']

class StatusFormulaireSerializer (serializers.ModelSerializer):
    class Meta :
        model = statusFormulaire
        fields = "__all__"


# serializer pour l'affichage et l'enregistrement de tout un formulaire, question et checbox

class CheckboxAllSerializer (serializers.ModelSerializer):
    class Meta :
        model = CheckBox
        fields = ['id', 'titre']

class QuestionAllSerializer (serializers.ModelSerializer):
    
    checkbox = CheckboxAllSerializer(many = True)
    class Meta :
        model = Question
        fields = ['id', 'titre', 'type', 'checkbox']

class FormulaireAllSerializer (serializers.ModelSerializer):
    question = QuestionAllSerializer(many = True)

    class Meta :
        model = Formulaire
        fields = "__all__"
    
    def create(self, validated_data):
        question_data = validated_data.pop('question')
        formulaire = Formulaire.objects.create(**validated_data)
        for question in question_data:
            checkbox_data = question.pop('checkbox')
            question_create = Question.objects.create(formulaire=formulaire, **question)
            for checkbox in checkbox_data :
                CheckBox.objects.create(question = question_create, **checkbox)
        return formulaire
    

# création des serializer adapaté à l'affichage des réponse du formulaire
class ResponseCheckboxAllSerializer (serializers.ModelSerializer):
    class Meta:
        model = ResponseCheckbox
        fields = ['id', 'id_etudiant', 'valeur']

class ResSerializer (serializers.ModelSerializer):
    id_etudiant = serializers.PrimaryKeyRelatedField(queryset = Etudiant.objects.all())
    class Meta :
        model = ResponseForm
        fields = ["id", "id_etudiant", "content"]

class CheckboxReSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()    
    class Meta:
        model = CheckBox
        fields = ['id', 'titre', 'response']
    
    def get_response (self, obj) :
        user_id = self.context.get('user_id')
        reponses = ResponseCheckbox.objects.filter(id_etudiant_id=user_id, checkbox=obj)
        return ResponseCheckboxAllSerializer(reponses, many=True).data

class QuestionResponseSerializer(serializers.ModelSerializer):
    responses = serializers.SerializerMethodField()
    checkbox = CheckboxReSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'titre', 'type', 'responses', 'checkbox']

    def get_responses(self, obj):
        user_id = self.context.get('user_id')
        reponses = ResponseForm.objects.filter(id_etudiant_id=user_id, question=obj)
        return ResSerializer(reponses, many=True).data

class FormulaireResponseSerializer(serializers.ModelSerializer):
    question = QuestionResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Formulaire
        fields = ['id', 'titre', 'description', 'session', 'profile', 'langue', 'question']   