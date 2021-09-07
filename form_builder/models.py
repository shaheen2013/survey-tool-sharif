from django.db import models
import json

class QuestionType(models.Model):
    choice = (
        ('checkbox', 'Multi choice'),
        ('date', "Date"),
        ('email', "Email"),
        ('file', "File"),
        ('number', "Number"),
        ('radio', "Radio select"),
        ('text', 'Single line answer'),
        ('time', "Time"),
        ('url', "Url"),
        ('week', "Week"),
        ('select', "Dropdown"),
        ('textarea', "Text")
    )
    title = models.CharField(max_length=50,null=True,blank=True)
    type = models.CharField(choices=choice,max_length=10,null=True,blank=True)
    options = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title or ""


class Survey(models.Model):
    title = models.CharField(max_length=150,blank=True,null=True)

    def __str__(self):
        return self.title or ""


class Question(models.Model):
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE)
    title = models.CharField(max_length=150,blank=True,null=True)
    type = models.CharField(max_length=100,blank=True,null=True)
    options = models.CharField(max_length=100,blank=True,null=True)
    choices = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title or ""

    def save(self, *args, **kwargs):
        choices = self.options.split(',')
        choice_dict = {}
        for choice in choices:
            key = choice
            choice_dict[key] = choice
        self.choices = json.loads(json.dumps(choice_dict))
        super(Question, self).save(*args, **kwargs)