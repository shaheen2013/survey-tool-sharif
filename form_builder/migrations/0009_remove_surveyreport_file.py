# Generated by Django 3.2.7 on 2021-09-10 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_builder', '0008_surveyreport_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyreport',
            name='file',
        ),
    ]
