from django.shortcuts import render, HttpResponse, redirect
from .serializers import QuestionTypeSerializer, SurveySerializer, QuestionSerializer
from django.views import generic
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .models import QuestionType, Survey, Question, SurveyReport
from rest_framework.response import Response
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class HomeView(generic.View):
    def get(self, request):
        return render(request, 'index.html')


class QuestionTypeView(APIView):
    def get(self, request, format=None):
        types = QuestionType.objects.all()
        serializer = QuestionTypeSerializer(types, many=True)
        return Response(serializer.data)


class SurveyView(APIView):
    def get(self, request, id):
        questions = Question.objects.filter(survey_id=id).values("id", "title", "type", "options").order_by('ordering')
        questions = list(questions)
        survey = list(Survey.objects.filter(id=id).values("id", "title"))
        final_list = questions + survey
        return Response(json.loads(json.dumps(final_list)))


class SurveySaveUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"info": "save", "message": "{} survey form has been saved successfully".format(request.data['title'])})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        survey_id = request.data.pop('survey_id')
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(survey_id, serializer.data)
            return Response(
                {"info": "update",
                 "message": "{} survey form has been updated successfully".format(request.data['title'])})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SurveyPreview(generic.View):
#
#     def get(self, request, id):
#         questions = Question.objects.filter(survey_id=id).order_by('ordering')
#         survey = Survey.objects.get(id=id)
#         return render(request, 'preview.html', {"questions": questions, "survey": survey})
#
#     def post(self, request, id):
#         # print("files ", request.FILES)
#         queryDict = dict(request.POST)
#         queryDict.pop('csrfmiddlewaretoken')
#         questions = list(
#             Question.objects.filter(survey_id=id).order_by('ordering').values('id', 'title', 'type', 'options'))
#         # print("others ", queryDict)
#         answers = []
#         # if len(questions) != len(queryDict.keys()):
#         #     return HttpResponse("All answer required")
#         i = 1
#         for question in questions:
#             data = {}
#             data['id'] = question['id']
#             data['question'] = question['title']
#             data['type'] = question['type']
#             data['options'] = question['options']
#             if question['type'] == 'file':
#                 data['answer'] = request.FILES.get(str(i)).name
#                 file = request.FILES.get(str(i))
#                 default_storage.save('media/' + request.FILES.get(str(i)).name, ContentFile(file.read()))
#             else:
#                 data['answer'] = queryDict.get(str(i))
#             i += 1
#             answers.append(data)
#         # print(answers)
#         report = SurveyReport(survey_id=id, survey_report=answers)
#         report.save()
#         return redirect('/survey-list')


class SurveyPreviewQuestion(APIView):
    def get(self, request, id):
        questions = Question.objects.filter(survey_id=id).values("id", "title", "type", "choices").order_by('ordering')
        return Response(questions)

class SurveyPreviewShow(generic.View):
    def get(self, request, id):
        survey = Survey.objects.get(id=id)
        return render(request, 'preview.html', {"id": id, "survey_title": survey.title})


class SurveyPreviewSave(APIView):
    def post(self, request, id):
        print("Post")


def surveyList(request):
    surveys = Survey.objects.all()
    return render(request, 'survey-list.html', {"surveys": surveys})


class UpdatePage(generic.View):
    def get(self, request, id):
        return render(request, 'edit-survey.html', {"id": id})
