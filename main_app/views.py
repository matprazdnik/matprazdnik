# Create your views here.
from django.shortcuts import render

from main_app.models import Participant, School


def attach_info(dict_):
    return dict({
        'num_participants': len(Participant.objects.all()),
    }, **dict_)



def participants(request):
    return render(request, 'participants.html', attach_info({
        'nav': 'participants',
    }))