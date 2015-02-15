from collections import defaultdict
import csv
import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from flying_rows.models import Transaction
from flying_rows.utils import get_model_class, convert_to_string

from main_app.models import Participant
from main_app.tables import RegistrationTableConfig, SchoolsTableConfig, ResultsTableConfig


MIN_SCORE = 8  # lower bound for diplomas bounds view


def participants(request):
    return render(request, 'participants.html', attach_info({
        'nav': 'participants',
        'table': RegistrationTableConfig
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
    if 'score' in request.GET:
        score = int(request.GET['score'])
        users = list(Participant.objects.filter(deleted=False, sum=score))
        users = sorted(users, key=lambda u: u.surname)
        return render(request, 'users_with_score.html', attach_info({
            "nav": "diplomas",
            "users": users,
            "score": score
        }))

    class Row:
        pass

    class Table:
        pass

    table = Table()
    scores = [int(participant.sum) if participant.sum is not None else 0
              for participant in Participant.objects.filter(deleted=False)]
    max_score = max(scores) if len(scores) > 0 else 0
    table.rows = [Row(), Row()]
    table.rows[0].name = '='
    table.rows[1].name = '>='
    print(table)

    scores_with_such_participants = [i for i in range(MIN_SCORE, max_score + 1) if len(Participant.objects.filter(sum=i)) > 0]
    table.columns = scores_with_such_participants
    table.rows[0].data = [len(list(Participant.objects.filter(sum=i))) for i in scores_with_such_participants]
    table.rows[1].data = [len(list(Participant.objects.filter(sum__gte=i))) for i in scores_with_such_participants]

    return render(request, 'diplomas.html', attach_info({
        'nav': 'diplomas',
        'table': table
    }))

def missing(request):
    users = list(x for x in Participant.objects.filter(deleted=False, sum=None) if x.test_number != "")
    users = sorted(users, key=lambda u: u.surname)
    return render(request, 'missing.html', attach_info({
        'nav': 'missing',
        'users': users,
        'missing_count': len(users)
    }))


def stats(request):
    class User:
        pass
    names = [x for x in list(set(y.author for y in Transaction.objects.all())) if x is not None and x != ""]

    def calc_stats_for_user(name):
        user = User()
        user.name = name
        rows = set([x.rowId for x in Transaction.objects.filter(author=name) if (x.column == 'test_number' or x.type == 'add_row')])

        def avg(x):
            if len(x) == 0:
                return 0
            return sum(x) / float(len(x))

        def median(x):
            if len(x) == 0:
                return 0
            return sorted(x)[len(x)//2]

        def calc_stats_by_minute(criteria):
            group_by_minutes = defaultdict(lambda: [])
            for transaction in Transaction.objects.filter(author=name):
                if not criteria(transaction):
                    continue
                time = transaction.timestamp
                time = (time.year, time.month, time.day, time.hour, time.minute)
                group_by_minutes[time].append(transaction.rowId)

            return avg([x for x in [len(set(v)) for v in group_by_minutes.values()] if x > 1])

        user.registrations = len(rows)
        user.registrations_per_minute = calc_stats_by_minute(lambda t: t.column == 'test_number' or t.type == 'add_row')
        rows = set([x.rowId for x in Transaction.objects.filter(author=name) if x.column == 'sum'])
        user.scores = len(rows)
        user.scores_per_minute = calc_stats_by_minute(lambda t: t.column == 'sum')
        return user

    stats = [calc_stats_for_user(name) for name in names]
    stats.sort(key=lambda x: x.registrations + x.scores, reverse=True)

    return render(request, 'stats.html', attach_info({
        'nav': 'stats',
        'stats': stats
    }))


def said_gender(gender):
    return 'ученик' if gender == 'м' else 'ученица'


def diplomas_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="diplomas.csv"'
    writer = csv.writer(response)
    columns = ['version_code', 'participant_code', 'test_number', 'name', 'surname',
               'gender', 'grade', 'school', 'sum',
               'points_1', 'points_2a', 'points_2b', 'points_3', 'points_4', 'points_5', 'points_6']
    writer.writerow(columns)
    for p in Participant.objects.filter(deleted=False).order_by('sum'):
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
        'num_participants': len(Participant.objects.filter(deleted=False)),
        'number_not_null': len([x for x in Participant.objects.filter(deleted=False)
                                if x.test_number is not None and x.test_number != '']),
        'participants_with_score': len([x for x in Participant.objects.filter(deleted=False)
                                        if x.sum is not None and x.sum != '']),
    }, **dict_)