# -*- coding: utf-8 -*-

import os
import re

from django.shortcuts import render

from main_app.models import Participant
from main_app.utils import attach_info


CURRENT_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

CONFIG_FILENAME = os.path.join(CURRENT_SCRIPT_DIR, 'bounds.config')


class BoundsConfig:
    def __init__(self, new_value=None):
        if new_value:
            with open(CONFIG_FILENAME, 'w') as fout:
                fout.write(new_value)

        with open(CONFIG_FILENAME) as fin:
            self.raw = fin.read()

        self.diploma_degree_by_score = {}
        self.degrees = []
        for line in self.raw.split('\n'):
            line = line.strip()
            if line:
                degree, scores = re.split('\s*:\s*', line)
                a, b = map(int, re.findall('\d+', scores))
                for i in range(a, b + 1):
                    self.diploma_degree_by_score[i] = degree
                self.degrees.append((degree, a, b + 1))

    def __getitem__(self, key):
       return self.diploma_degree_by_score.get(key, '')


class Row:
    pass

class Table:
    def __init__(self):
        self.rows = []


def diplomas(request):
    if request.method == 'POST':
        bounds_config = BoundsConfig(request.POST['bounds_config'])
        # TODO: return redirect to GET /diplomas (POST-REDIRECT-GET pattern)
    else:
        bounds_config = BoundsConfig()

    table = Table()
    scores = [int(participant.sum) if participant.sum is not None else 0 for participant in Participant.objects.all()]
    max_score = max(scores) if len(scores) > 0 else 0

    table.columns = ['набрали ровно столько', 'набрали хотя бы столько', 'диплом']
    for i in range(max_score, -1, -1):
        row = Row()
        row.name = str(i)
        row.data = [len(list(Participant.objects.filter(sum=i))),
            len(list(Participant.objects.filter(sum__gte=i))), 
            bounds_config[i]
        ]
        table.rows.append(row)

    degree_owners = [
        (degree, Participant.objects.filter(sum__gt=lower_bound - 1, sum__lt=upper_bound + 1).count())
        for degree, lower_bound, upper_bound in bounds_config.degrees
    ]

    return render(request, 'diplomas.html', attach_info({
        'nav': 'diplomas',
        'table': table,
        'bounds_config_raw': bounds_config.raw,
        'degree_owners': degree_owners,
    }))
