from django import forms
from .models import Question, SurveyReport


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['id', 'title', 'type', 'choices']


class SurveyReportForm(forms.ModelForm):
    class Meta:
        model = SurveyReport
        fields = ['survey', 'survey_report']

    def clean(self):
        for item in self.cleaned_data['survey_report']:
            print(item.get('answer'))

            # if item.get('answer') == None:
            #     raise ValidationError('Answer must be required')
