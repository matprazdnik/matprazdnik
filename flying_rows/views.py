from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.db import models

import importlib
import json


from .utils import is_foreign_key, get_field_by_name, get_field_value, get_foreign_key


def get_model_class(request):
    method = request.method
    module_name = getattr(request, method)['module']
    model_name = getattr(request, method)['model']
    module = importlib.import_module(module_name)
    return getattr(module, model_name)

def convert_value_to_string(value):
    return str(value) if value is not None else ''

def load_new_rows(request):
    # ajax request
    # params: [highest_loaded_id, module, model, columns_space_delimited]
    if request.method == 'GET':
        highest_loaded_id = request.GET['highest_loaded_id']
        column_ordering = request.GET['columns_space_delimited'].split() + ['id']
        model_class = get_model_class(request)

        objs = model_class.objects.filter(id__gt=highest_loaded_id)
        response_data = {}
        for obj in objs:
            response_data[obj.id] = {}
            for column in column_ordering:
                response_data[obj.id][column] = convert_value_to_string(getattr(obj, column))
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponseNotAllowed(["GET"])

def load_autocomplete_choices(request):
    # ajax request
    # params: [module, model, columns_space_delimited]
    # returns: json mapping column_name -> array of possible values
    if request.method == 'GET':
        model_class = get_model_class(request)
        column_names = request.GET['columns_space_delimited'].split()
        response_data = {}
        for column_name in column_names:
            response_data[column_name] = []
            if is_foreign_key(column_name, model_class):
                foreign_key_model_class = get_field_by_name(column_name, model_class).related.parent_model
                response_data[column_name] = [str(i) for i in foreign_key_model_class.objects.all()]
            else:
                response_data[column_name] = list(set([str(getattr(i, column_name)) for i in model_class.objects.all()]))
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponseNotAllowed(["GET"])

def get_search_hints(request):
    # ajax request
    # params: [module, model, search_fields_space_delimited]
    # returns: search_hints array
    if request.method == 'GET':
        model_class = get_model_class(request)
        search_fields = request.GET['search_fields_space_delimited'].split()
        values = [ ' '.join([str(getattr(object, search_field)) for search_field in search_fields]) for object in model_class.objects.all() ]
        values = list(set(values))
        return HttpResponse(json.dumps({ 'search_hints': values}), content_type = 'application/json')
    else:
        return HttpResponseNotAllowed(["GET"])



def search(request):
    if request.method == 'GET':
        model_class = get_model_class(request)
        search_fields = request.GET['search_fields_space_delimited'].split()
        objects = [ (' '.join([str(getattr(object, search_field)) for search_field in search_fields]), object) for object in model_class.objects.all() ]
        search_value = request.GET['search_value']
        equal_objects = list(filter(lambda x: x[0] == search_value, objects))
        like_objects = list(filter(lambda x: search_value in x[0], objects))
        not_really_like_objects = objects
        for search_value_part in search_value.split():
            not_really_like_objects = filter(lambda x: search_value_part in x[0], not_really_like_objects)
        not_really_like_objects = list(not_really_like_objects)
        if len(equal_objects) == 1:
            return HttpResponse(json.dumps({ 'success' : True, 'row_id': equal_objects[0][1].id }), content_type='application/json')
        elif len(like_objects) == 1:
            return HttpResponse(json.dumps({ 'success' : True, 'row_id': like_objects[0][1].id }), content_type='application/json')
        elif len(not_really_like_objects) == 1:
            return HttpResponse(json.dumps({ 'success' : True, 'row_id': not_really_like_objects[0][1].id }), content_type='application/json')
        elif len(not_really_like_objects) > 1:
            return HttpResponse(json.dumps({ 'success' : False, 'error_message': 'Несколько таких объектов' }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({ 'success' : False, 'error_message': 'Нет таких объектов' }), content_type='application/json')
    else:
        return HttpResponseNotAllowed(["GET"])

@csrf_exempt
def update_field(request):
    # ajax request
    # params: [row_id, field_name, new_field_value, module, model]
    if request.method == "POST":
        try:
            model_class = get_model_class(request)
            obj = model_class.objects.get(id=request.POST['row_id'])
            column_name = request.POST['field_name']
            value = request.POST['new_field_value'].strip()
            if is_foreign_key(column_name, model_class):
                # TODO: resolve foreign_key problem
                value = get_foreign_key(column_name, model_class, value)
                #   value = getattr(model_class, column_name).get_query_set()[0]
            setattr(obj, column_name, value)
            obj.save();
            response_data = {'success' : True, 'value': str(value) }
            return HttpResponse(json.dumps(response_data), content_type = 'application/json');
        except Exception as e:
            response_data = {'success': False, 'error_message': str(e)  }
            return HttpResponse(json.dumps(response_data), content_type = 'application/json');
    else:
        return HttpResponseNotAllowed(["POST"])


@csrf_exempt
def add_new_row(request):
    # ajax request
    # params: [module, model, columns_space_delimited, new_row_values]
#    return HttpResponse(json.dumps({}), content_type = 'application/json')
    if request.method == "POST":
        try:
            column_ordering = request.POST['columns_space_delimited'].split()
            model_class = get_model_class(request)
            new_obj = model_class()
            for column_name in column_ordering:
                if is_foreign_key(column_name, model_class):
                    # TODO: resolve foreign_key problem
                    value = get_foreign_key(column_name, model_class, request.POST[column_name])
                    # value = getattr(model_class, column_name).get_query_set()[0]
                else:
                    value = get_field_value(column_name, model_class, request.POST[column_name])
                setattr(new_obj, column_name, value)
            new_obj.save()
            response_data = { 'success': True }
            return HttpResponse(json.dumps(response_data), content_type = 'application/json')
        except Exception as e:
            response_data = { 'success': False, 'error_message': str(e) }
            return HttpResponse(json.dumps(response_data), content_type = 'application/json')
    else:
        return HttpResponseNotAllowed(["POST"])