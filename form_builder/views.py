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


# @method_decorator(csrf_exempt, name='dispatch')
# class SurveyView(generic.CreateView):
#     def post(self, request):
#         data = {}
#         infos = json.loads(request.body.decode("utf-8").replace("'", '"'))
#         data['title'] = infos[len(infos)-1]['survey_title']
#         infos.pop(len(infos)-1)
#         data['questions'] = infos
#         serializer = SurveySerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse("{} survey form has been saved successfully".format(data['title']))
#         return HttpResponse(serializer.errors['non_field_errors'][0])


@method_decorator(csrf_exempt, name='dispatch')
class SurveyView(generic.CreateView,generic.UpdateView):
    def post(self, request):
        data = {}
        infos = json.loads(request.body.decode("utf-8").replace("'", '"'))
        data['title'] = infos[len(infos)-1]['survey_title']
        infos.pop(len(infos)-1)
        data['questions'] = infos
        serializer = SurveySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json.dumps({"info":"save","message":"{} survey form has been saved successfully".format(data['title'])}))
        return HttpResponse(json.dumps(serializer.errors))

    def put(self,request, *args, **kwargs):
        data = {}
        infos = json.loads(request.body.decode("utf-8").replace("'", '"'))
        survey_id = infos.pop(len(infos)-1)
        data['title'] = infos[len(infos) - 1]['survey_title']
        infos.pop(len(infos) - 2)
        data['questions'] = infos
        serializer = SurveySerializer(data=data)
        if serializer.is_valid():
            serializer.update(survey_id,serializer.data)
            return HttpResponse(json.dumps(
                {"info": "update", "message": "{} survey form has been updated successfully".format(data['title'])}))
        else:
            print(serializer.errors)
        return HttpResponse(json.dumps(serializer.errors))


def SurveyPreview(request, id):
    questions = Question.objects.filter(survey_id=id)
    survey = Survey.objects.get(id=id)
    return render(request, 'preview.html', {"questions": questions, "survey": survey})


def surveyList(request):
    surveys = Survey.objects.all()
    return render(request, 'survey-list.html', {"surveys": surveys})



class UpdatePage(generic.View):
    def get(self,request,id):
        return render(request, 'edit-survey.html',{"id":id})


class SurveyUpdateView(generic.View):
    def get(self,request, id):
        questions = Question.objects.filter(survey_id=id).values("id","title","type","options")
        questions = list(questions)
        survey = list(Survey.objects.filter(id=id).values("id","title"))
        final_list = questions+survey
        # print(final_list)
        # questions.append(survey)
        # print(questions)
        return HttpResponse(json.dumps(final_list))

    def post(self,request):
        print("post value")


