# Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response

from main_app.models import Participant, School


def attach_info(dict_):
    return dict({
        'num_participants': len(Participant.objects.all()),
    }, **dict_)



def participants(request):
    return render(request, 'participants.html', attach_info({
        'nav': 'participants',
    }))


def schools(request):
    return render(request, 'schools.html', attach_info({
        'nav': 'schools',
        }))


def points(request):
    return render(request, 'points.html', attach_info({
        'nav': 'points',
        }))


def diplomas(request):
    return render(request, 'diplomas.html', attach_info({
        'nav': 'diplomas',
        }))