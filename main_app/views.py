import csv
import datetime

from django.shortcuts import render
from django.http import HttpResponse

from main_app.models import Participant
from main_app.tables import RegistrationTableConfig, SchoolsTableConfig, ResultsTableConfig
from main_app.utils import attach_info


def participants(request):
    return render(request, 'participants.html', attach_info({
        'nav': 'participants',
        'table': RegistrationTableConfig,
    }))


def schools(request):
    return render(request, 'schools.html', attach_info({
        'nav': 'schools',
        'table': SchoolsTableConfig,
    }))


def points(request):
    return render(request, 'points.html', attach_info({
        'nav': 'points',
        'table': ResultsTableConfig,
    }))


def said_gender(gender):
    return 'ученик' if gender == 'м' else 'ученица'


def diplomas_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="diplomas.csv"'
    writer = csv.writer(response)
    columns = ['version_code', 'participant_code', 'test_number', 'name', 'surname',
               'said_gender gender', 'gender', 'grade', 'school', 'sum',
               'points_1', 'points_2', 'points_3a', 'points_3b', 'points_4', 'points_5', 'points_6']
    writer.writerow(columns)
    for p in Participant.objects.all().order_by('sum'):
        # if not p.sum:
        #     continue
        row = [(globals()[column.split()[0]](getattr(p, column.split()[1]))
               if ' ' in column else getattr(p, column))
               for column in columns]
        row = [str(x).strip() for x in row]
        writer.writerow(row)
    return response
