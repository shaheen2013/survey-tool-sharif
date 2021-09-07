import serializers as serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import QuestionType,Survey,Question
from rest_framework import serializers


class QuestionTypeSerializer(ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ['id','title','type','options']


# class QuestionSerializer(ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['title','type','options']


    # def validate(self, data):
    #     # if len(data) == 0:
    #     #     raise ValidationError("At least one question required")
    #     index = 1
    #     for question in data:
    #         print(question[2])
    #         # if question[0] == '':
    #         #     raise ValidationError("Question {}'s title must be required".format(index))
    #         if question[1] == 'checkbox' or question[1] == 'select' or question[1] == 'radio':
    #             if question[2] == '':
    #                 raise ValidationError("Options of question {} must be required".format(index))
    #         index += 1
    #     return data



# class SurveySerializer(ModelSerializer):
#     questions = QuestionSerializer(many=True)
#
#     class Meta:
#         model = Survey
#         fields = ['title','questions']
#
#     def validate(self, data):
#         print("type of data, ",type(data))
#         if data.get('title') == "":
#             raise ValidationError("Survey name must be required")
#         questions = data.get('questions')
#         if len(questions) == 0:
#             raise ValidationError("At least one question required")
#         index = 1
#         for question in questions:
#             if question['title'] == '':
#                 raise ValidationError("Question {}'s title must be required".format(index))
#             if question['type'] == 'checkbox' or question['type'] == 'select' or question['type'] == 'radio':
#                 if question['options'] == '':
#                     raise ValidationError("Options of question {} must be required".format(index))
#             index += 1
#         return data
#
#     def create(self, validated_data):
#         questions_data = validated_data.pop('questions')
#         survey = Survey.objects.create(**validated_data)
#         for question in questions_data:
#             Question.objects.create(survey=survey, **question)
#         return survey


class QuestionSerializer(serializers.Serializer):
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
        for question in questions_data:
            Question.objects.create(survey=survey, **question)
        return survey

    def update(self,survey_id, validated_data):
        print("updated ",validated_data)
        survey = Survey.objects.get(id=survey_id)
        survey.delete()
        self.create(validated_data)

