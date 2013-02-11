# Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt


from main_app.models import Participant, School
from main_app.tables import RegistrationTableConfig


def attach_info(dict_):
    return dict({
        'num_participants': len(Participant.objects.all()),
    }, **dict_)


def participants(request):
    return render(request, 'participants.html', attach_info({
        'nav': 'participants',
        'table': RegistrationTableConfig,
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

@csrf_exempt
def update_participants(request): # ajax update request
    if request.method == "POST":
        try:
            p = Participant.objects.get(id=request.POST['row_id']);
        except Participant.DoesNotExist:
            return Http404();
        for key in request.POST:
            try:
                setattr(p, key, request.POST[key])
            except:
                pass
        try:
            p.save();
            return HttpResponse('');
        except Exception as e:
            print(e)
            return HttpResponseNotAllowed(['POST']);
    else:
        return Http404();