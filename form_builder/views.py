from django.shortcuts import render, HttpResponse, redirect
from .serializers import QuestionTypeSerializer, SurveySerializer, QuestionSerializer
from django.views import generic
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import QuestionType, Survey, Question
from rest_framework.response import Response
import json


class HomeView(generic.View):
    def get(self, request):
        return render(request, 'index.html')


class QuestionTypeView(APIView):
    def get(self, request, format=None):
        types = QuestionType.objects.all()
        serializer = QuestionTypeSerializer(types, many=True)
        return Response(serializer.data)


class SurveyView(GenericAPIView):

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
                {"info": "update", "message": "{} survey form has been updated successfully".format(request.data['title'])})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def SurveyPreview(request, id):
    questions = Question.objects.filter(survey_id=id).order_by('ordering')
    survey = Survey.objects.get(id=id)
    return render(request, 'preview.html', {"questions": questions, "survey": survey})


def surveyList(request):
    surveys = Survey.objects.all()
    return render(request, 'survey-list.html', {"surveys": surveys})


class UpdatePage(generic.View):
    def get(self, request, id):
        return render(request, 'edit-survey.html', {"id": id})


class SurveyUpdateView(generic.View):
    def get(self, request, id):
        questions = Question.objects.filter(survey_id=id).values("id", "title", "type", "options").order_by('ordering')
        questions = list(questions)
        survey = list(Survey.objects.filter(id=id).values("id", "title"))
        final_list = questions + survey
        return HttpResponse(json.dumps(final_list))

    def post(self, request):
        print("post value")
