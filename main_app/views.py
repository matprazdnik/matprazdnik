import csv
import datetime

from django.shortcuts import render
from django.http import HttpResponse

from main_app.models import Participant
from main_app.tables import RegistrationTableConfig, SchoolsTableConfig, ResultsTableConfig


MIN_SCORE = 8  # lower bound for diplomas bounds view


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


def diplomas(request):
    class Row:
        pass

    class Table:
        pass

    table = Table()
    scores = [int(participant.sum) if participant.sum is not None else 0 for participant in Participant.objects.all()]
    max_score = max(scores) if len(scores) > 0 else 0
    table.rows = [Row(), Row()]
    table.rows[0].name = '='
    table.rows[1].name = '>='

    scores_with_such_participants = [i for i in range(MIN_SCORE, max_score + 1) if len(Participant.objects.filter(sum=i)) > 0]
    table.columns = scores_with_such_participants
    table.rows[0].data = [len(list(Participant.objects.filter(sum=i))) for i in scores_with_such_participants]
    table.rows[1].data = [len(list(Participant.objects.filter(sum__gte=i))) for i in scores_with_such_participants]

    return render(request, 'diplomas.html', attach_info({
        'nav': 'diplomas',
        'table': table
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


# === Utils ===

def normalize_school(s):
    return str(s).replace(', г. Москва', '').replace(', г. Зеленоград', '')


def attach_info(dict_):
    return dict({
        'num_participants': len(Participant.objects.all()),
        'number_not_null': len([x for x in Participant.objects.all() if x.test_number is not None and x.test_number != '']),
        'participants_with_score': len([x for x in Participant.objects.all() if x.sum is not None and x.sum != '']),
    }, **dict_)
