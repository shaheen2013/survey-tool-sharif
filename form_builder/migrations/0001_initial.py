# Generated by Django 3.2.7 on 2021-09-03 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, choices=[('checkbox', 'Multi choice'), ('date', 'Date'), ('email', 'Email'), ('file', 'File'), ('number', 'Number'), ('radio', 'Radio select'), ('text', 'Single line answer'), ('time', 'Time'), ('url', 'Url'), ('week', 'Week'), ('select', 'Dropdown'), ('textarea', 'Text')], max_length=10, null=True)),
                ('options', models.TextField(blank=True, null=True)),
                ('choices', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
