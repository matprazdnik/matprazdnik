from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.db import models

import importlib
import json


from .utils import is_foreign_key, get_field_by_name, convert_value_to_field_type


def get_model_class(request):
    method = request.method
    module_name = getattr(request, method)['module']
    model_name = getattr(request, method)['model']
    module = importlib.import_module(module_name)
    return getattr(module, model_name)


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
                response_data[obj.id][column] = str(getattr(obj, column))
        return HttpResponse(json.dumps(response_data), content_type='application/json')
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
            value = request.POST['new_field_value']
            if is_foreign_key(column_name, model_class):
                # TODO: resolve foreign_key problem
                value = getattr(model_class, column_name).get_query_set()[0]
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
                    value = getattr(model_class, column_name).get_query_set()[0]
                else:
                    value = convert_value_to_field_type(request.POST[column_name],
                        get_field_by_name(column_name, model_class))
                setattr(new_obj, column_name, value)
            new_obj.save()
            response_data = { 'success': True }
            return HttpResponse(json.dumps(response_data), content_type = 'application/json')
        except Exception as e:
            response_data = { 'success': False, 'error_message': str(e) }
            return HttpResponse(json.dumps(response_data), content_type = 'application/json')
    else:
        return HttpResponseNotAllowed(["POST"])