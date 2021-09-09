from rest_framework.serializers import ModelSerializer, ValidationError
from .models import QuestionType, Survey, Question
from rest_framework import serializers


class QuestionTypeSerializer(ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ['id', 'title', 'type', 'options']


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=100, required=True)
    type = serializers.CharField(required=True)
    options = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs['type'] == 'checkbox' or attrs['type'] == 'select' or attrs['type'] == 'radio':
            if attrs['options'] == "":
                raise ValidationError("Options of question must be required")
        return attrs


class SurveySerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    questions = serializers.ListField(
        child=(QuestionSerializer()),
        allow_empty=False
    )

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        survey = Survey.objects.create(**validated_data)
        i = 1
        for question in questions_data:
            Question.objects.create(survey=survey, title=question['title'], type=question['type'],
                                    options=question['options'], ordering=i)
            i += 1
        return survey

    def update(self, survey_id, validated_data):
        questions_data = validated_data.pop('questions')
        survey = Survey.objects.get(id=survey_id)
        survey.title = validated_data['title']
        survey.save()
        questions_list = []
        i = 1
        for question in questions_data:
            obj, created = Question.objects.update_or_create(
                id=question.get('id'),
                defaults={
                    'survey': survey,
                    'title': question['title'],
                    'type': question['type'],
                    'options': question['options'],
                    'ordering': i
                }
            )
            questions_list.append(obj.id)
            i += 1
        questions = Question.objects.filter(survey_id=survey_id).exclude(id__in=questions_list)
        questions.delete()
        return survey
