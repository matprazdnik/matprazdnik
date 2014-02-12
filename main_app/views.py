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
    max_score = max([int(participant.sum) if participant.sum is not None else 0 for participant in Participant.objects.all()])
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


def diplomas_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="diplomas.csv"'
    writer = csv.writer(response)
    for p in Participant.objects.all():
        writer.writerow(list(map(str, [
            p.name, p.surname, p.gender, p.points_1, p.points_2, p.points_3,
            p.points_4, p.points_5, p.points_6, normalize_school(p.school),
            p.grade, p.sum
        ])))
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
