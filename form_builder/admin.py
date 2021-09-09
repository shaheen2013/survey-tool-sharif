from django.contrib import admin

from .models import QuestionType, Survey, Question, SurveyReport

admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(SurveyReport)


class QuestionInLineModel(admin.StackedInline):
    model = Question
    fields = ['survey', 'title', 'type', 'options', 'ordering']
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    fields = ['title']
    inlines = [
        QuestionInLineModel,
    ]
