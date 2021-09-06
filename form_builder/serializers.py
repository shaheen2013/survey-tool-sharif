import serializers as serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import QuestionType,Survey,Question
from rest_framework import serializers


class QuestionTypeSerializer(ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ['id','title','type','options']


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ['title','type','options']


class SurveySerializer(ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['title','questions']

    def validate(self, data):
        if data.get('title') == "":
            raise ValidationError("Survey name must be required")
        questions = data.get('questions')
        if len(questions) == 0:
            raise ValidationError("At least one question required")
        for question in questions:
            if question['title'] == '':
                raise ValidationError("Question title must be required")
            if question['type'] == 'checkbox' or question['type'] == 'select' or question['type'] == 'radio':
                if question['options'] == '':
                    raise ValidationError("Options must be required")
        return data

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        survey = Survey.objects.create(**validated_data)
        for question in questions_data:
            Question.objects.create(survey=survey,**question)
        return survey


