from django.contrib import admin

# Register your models here.
from .models import QuestionType,Survey,Question

admin.site.register(QuestionType)
admin.site.register(Question)

class QuestionInLineModel(admin.StackedInline):
    model = Question
    fields = ['survey','title','type','options']
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    fields = ['title']
    inlines = [
        QuestionInLineModel,
    ]