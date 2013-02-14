# Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from main_app.models import Participant, School
from main_app.tables import RegistrationTableConfig
from flying_rows.models import ParticipantUpdateTime

import datetime
import json

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

def timestamp():
    return int(datetime.datetime.now().strftime("%s"))

def update_participant_update_time(p):
    try:
        pud = ParticipantUpdateTime.objects.get(participant = p);
        pud.last_update_time = timestamp();
        pud.save();
    except:
        pud = ParticipantUpdateTime(participant = p, last_update_time = timestamp());
        pud.save();
    print(pud);

#@csrf_exempt
#def update_participants(request): # ajax update request
#    if request.method == "POST":
#        try:
#            p = Participant.objects.get(id=request.POST['row_id']);
#        except Participant.DoesNotExist:
#            return Http404();
#        try:
#            field_name = request.POST['field_name'];
#        except KeyError:
#            return Http404();
#        old_field_value = p.__getattribute__(field_name);
#        try:
#            new_field_value = request.POST['new_field_value'];
#        except KeyError:
#            return Http404();
#        try:
#            setattr(p, field_name, new_field_value)
#            p.save();
#            update_participant_update_time(p);
#            response_data = {'success' : 'true', 'value': new_field_value }
#            return HttpResponse(json.dumps(response_data), content_type = 'application/json');
#        except Exception as e:
#            response_data = {'success': 'false', 'value': old_field_value }
#            return HttpResponse(json.dumps(response_data), content_type = 'application/json');
#    else:
#        return HttpResponseNotAllowed(["POST"])
#
#def get_school(school_name):
#    try:
#        return School.objects.get(genitive=school_name)
#    except:
#        return School.objects.get(genitive__contains=school_name)
#
#@csrf_exempt
#def add_participants(request): # ajax add request
#    if request.method == "POST":
#        try:
#            params = {key : request.POST[key] for key in request.POST};
#            try:
#                params['school'] = get_school(params['school']);
#            except:
#                response_data = { 'success': 'false', 'error_message': 'Неправильное название школы "' + params['school'] + '"'}
#                return HttpResponse(json.dumps(response_data), content_type = 'application/json');
#            p = Participant(**params);
#            p.save();
#            update_participant_update_time(p);
#            response_data = { 'success': 'true' }
#            response_data['row_id'] = p.id;
#            for key in params:
#                response_data[key] = str(params[key]);
#                update_participant_update_time
#            return HttpResponse(json.dumps(response_data), content_type = 'application/json');
#        except Exception as e:
#            response_data = { 'success': 'false', 'error_message': str(e) }
#            return HttpResponse(json.dumps(response_data), content_type = 'application/json');
#    else:
#        return HttpResponseNotAllowed(["POST"])