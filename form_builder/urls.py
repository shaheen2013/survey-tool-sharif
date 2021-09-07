from django.urls import path

from form_builder.views import HomeView,QuestionTypeView,SurveyView,SurveyPreview,surveyList,SurveyUpdateView,UpdatePage

urlpatterns = [
    path('', HomeView.as_view()),
    path('question-type',QuestionTypeView.as_view()),
    path('survey-save/',SurveyView.as_view()),
    path('preview/<int:id>',SurveyPreview),
    path('survey-list',surveyList),
    path('update/<int:id>',UpdatePage.as_view()),
    path('update-survey/<int:id>',SurveyUpdateView.as_view())
]
