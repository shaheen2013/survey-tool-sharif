# Generated by Django 3.2.7 on 2021-09-10 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_builder', '0007_surveyreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyreport',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
    ]