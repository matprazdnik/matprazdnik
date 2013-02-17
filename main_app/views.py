# Create your views here.
from django.shortcuts import render, render_to_response

from main_app.models import Participant
from main_app.tables import RegistrationTableConfig, SchoolsTableConfig, ResultsTableConfig
from flying_rows.models import ParticipantUpdateTime
import csv
from django.http import HttpResponse


import datetime


def attach_info(dict_):
    return dict({
        'num_participants': len(Participant.objects.all()),
        'number_not_null': len(list(filter(lambda x: x.number is not None and x.number != '',Participant.objects.all()))),
        'participants_with_score': len(list(filter(lambda x: x.sum is not None and x.sum != '', Participant.objects.all())))
    }, **dict_)


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
    table.rows[0].data = [len(list(Participant.objects.filter(sum=i))) for i in range(0, max_score + 1)]
    table.rows[1].data = [len(list(Participant.objects.filter(sum__gte=i))) for i in range(0, max_score + 1)]
    table.columns = [i for i in range(0, max_score + 1)]

    return render(request, 'diplomas.html', attach_info({
        'nav': 'diplomas',
        'table': table
        }))

def diplomas_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="diplomas.csv"'
    writer = csv.writer(response)
    for p in Participant.objects.all():
        writer.writerow(list(map(str, [p.name, p.surname, p.gender, p.school, p.grade, p.sum])))
    return response

def timestamp():
    return int(datetime.datetime.now().strftime("%s"))

def update_participants(request):
    # fields: school name surname
    return

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