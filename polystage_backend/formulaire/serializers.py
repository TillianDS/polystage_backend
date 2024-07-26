from rest_framework import serializers
from formulaire.models import *

class FormulaireSerializer (serializers.ModelSerializer):
    date_limite = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', input_formats=['%d-%m-%Y %H:%M:%S'])
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
        fields = ['id', 'stage', 'checkbox', 'valeur']
        
class ResponseSerializer (serializers.ModelSerializer):
    #id_stage = serializers.PrimaryKeyRelatedField(queryset = Stage.objects.all())
    #question = serializers.PrimaryKeyRelatedField(queryset = Question.objects.all())
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
        model = StatusFormulaire
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
        fields = ['id', 'titre', 'type', 'checkbox', 'obligatoire']

class FormulaireAllSerializer (serializers.ModelSerializer):
    question = QuestionAllSerializer(many = True)
    date_limite = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', input_formats=['%d-%m-%Y %H:%M:%S'])
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
    

# ----------- serializer adapaté à l'affichage des réponse du formulaire----------------
class ResponseCheckboxAllSerializer (serializers.ModelSerializer):
    class Meta:
        model = ResponseCheckbox
        fields = ['id', 'stage', 'valeur']

class ResSerializer (serializers.ModelSerializer):
    class Meta :
        model = ResponseForm
        fields = ["id", "stage", "content"]

class CheckboxReSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()    
    class Meta:
        model = CheckBox
        fields = ['id', 'titre', 'response']
    
    def get_response (self, obj) :
        id_stage = self.context.get('id_stage')
        try :
            response = ResponseCheckbox.objects.get(stage=id_stage, checkbox=obj)
        except ResponseCheckbox.DoesNotExist:
            return None
        return ResponseCheckboxAllSerializer(response).data

class QuestionResponseSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()
    checkbox = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id', 'titre', 'type', 'obligatoire', 'response', 'checkbox']

    def get_response(self, obj):
        id_stage = self.context.get('id_stage')
        try :
            reponse = ResponseForm.objects.get(stage=id_stage, question=obj)
            return ResSerializer(reponse).data
        except :
            return None
        
    def get_checkbox (self, obj):
        if obj.type == 'checkbox':
            checkBox = CheckBox.objects.filter(question = obj)
            return CheckboxReSerializer(checkBox, many=True, read_only=True).data
        return None

class FormulaireResponseSerializer(serializers.ModelSerializer):
    question = QuestionResponseSerializer(many=True, read_only=True)
    date_limite = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', input_formats=['%d-%m-%Y %H:%M:%S'])

    class Meta:
        model = Formulaire
        fields = ['id', 'titre', 'description', 'session', 'profile', 'langue', 'question', 'date_limite']   