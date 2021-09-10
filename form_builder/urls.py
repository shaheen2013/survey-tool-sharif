from django.urls import path

from form_builder.views import HomeView, QuestionTypeView, SurveyView, SurveyPreviewShow, surveyList, \
    UpdatePage, SurveySaveUpdateView, SurveyPreviewQuestion

urlpatterns = [
    path('', HomeView.as_view()),
    path('question-type', QuestionTypeView.as_view()),
    path('survey/', SurveySaveUpdateView.as_view()),
    path('survey/<int:id>', SurveyView.as_view()),
    path('survey-list', surveyList),
    path('preview/<int:id>', SurveyPreviewShow.as_view()),
    path('preview-questions/<int:id>',SurveyPreviewQuestion.as_view()),
    path('update/<int:id>', UpdatePage.as_view()),

]
