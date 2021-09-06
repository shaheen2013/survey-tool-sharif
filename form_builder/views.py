from django.shortcuts import render,HttpResponse,redirect
from .serializers import QuestionTypeSerializer,SurveySerializer,QuestionSerializer
from django.views import generic
from rest_framework.views import APIView
from rest_framework import generics,status
from .models import QuestionType, Survey, Question
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


class HomeView(generic.View):
    def get(self,request):
        return render(request, 'index.html')



class QuestionTypeView(APIView):
    def get(self, request, format=None):
        types = QuestionType.objects.all()
        serializer = QuestionTypeSerializer(types, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class SurveyView(generic.CreateView):
    def post(self, request):
        data = {}
        infos = json.loads(request.body.decode("utf-8").replace("'",'"'))
        data['title'] = infos[len(infos)-1]['survey_title']
        infos.pop(len(infos)-1)
        data['questions'] = infos
        serializer = SurveySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("save")
        # print(serializer.errors['non_field_errors'][0])
        return HttpResponse(serializer.errors['non_field_errors'][0])


def SurveyPreview(request,id):
    questions = Question.objects.filter(survey_id=id)
    survey = Survey.objects.get(id=id)
    return render(request,'preview.html',{"questions":questions,"survey":survey})


def surveyList(request):
    surveys = Survey.objects.all()
    return render(request,'survey-list.html',{"surveys":surveys})


