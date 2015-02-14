# -*- coding: utf-8 -*-


import json
from django.db import transaction

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from flying_rows.models import Transaction

from .utils import (is_foreign_key, get_field_by_name, get_field_value,
                    get_foreign_key, get_model_class_from_request, convert_to_string,
                    join_obj_fields, autocomplete_choices)


NEW_ROWS_CHUNK_SIZE = 50

@require_GET
def load_new_rows(request):
    # ajax request
    # params: [module, model, highest_loaded_id, columns_space_delimited]
    # return: {object id: object column values}
    highest_loaded_id = request.GET['highest_loaded_id']
    columns = json.loads(request.GET['columns'])
    model_class = get_model_class_from_request(request)

    objs = model_class.objects.filter(id__gt=highest_loaded_id).order_by('id')[:NEW_ROWS_CHUNK_SIZE]
    response_data = []
    for obj in objs:
        response_data.append({
            'id': obj.id,
            'data': { column:  convert_to_string(getattr(obj, column))
                      for column in columns
            }
        })
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@require_GET
def load_autocomplete_choices(request):
    # ajax request
    # params: [module, model, column]
    # returns: {column_name: array of possible values}

    model_class = get_model_class_from_request(request)
    column = request.GET['column']
    return HttpResponse(json.dumps(autocomplete_choices(column, model_class)), content_type='application/json')

@require_GET
def get_search_hints(request):
    # ajax request
    # params: [module, model, search_fields_space_delimited]
    # return: [search_hints]
    model_class = get_model_class_from_request(request)
    search_fields = request.GET['search_fields_space_delimited'].split()
    # TODO: should we replace str() by convert_value_to_string()?
    values = [join_obj_fields(obj, search_fields) for obj in model_class.objects.all()]
    values = list(set(values))
    return HttpResponse(json.dumps({'search_hints': values}), content_type='application/json')


@require_GET
def search(request):
    # ajax request
    # params: [module, model, search_fields_space_delimited]
    # return: success (True/False), row_id
    # TODO: fill params and return
    model_class = get_model_class_from_request(request)
    search_fields = request.GET['search_fields_space_delimited'].split()
    objects = [(join_obj_fields(obj, search_fields), obj)
               for obj in model_class.objects.all()]
    search_value = request.GET['search_value']
    equal_objects = [x for x in objects if x[0] == search_value]
    like_objects = [x for x in objects if search_value in x[0]]
    not_really_like_objects = objects
    for search_value_part in search_value.split():
        not_really_like_objects = [x for x in not_really_like_objects if search_value_part in x[0]]
    if len(equal_objects) >= 1:
        response_data = {'success': True, 'row_id': equal_objects[0][1].id}
    elif len(like_objects) >= 1:
        response_data = {'success': True, 'row_id': like_objects[0][1].id}
    elif len(not_really_like_objects) >= 1:
        response_data = {'success': True, 'row_id': not_really_like_objects[0][1].id}
    elif len(not_really_like_objects) > 1:
        response_data = {'success': False,
                         'error_message': 'Поиск возвратил несколько объектов: {0}'.format(
                             ', '.join(str(obj) for obj in not_really_like_objects))}
    else:
        response_data = {'success': False, 'error_message': 'Нет таких объектов'}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@require_POST
@csrf_exempt
def update_field(request):
    # ajax request
    # params: [row_id, column, value, module, model]
    # return: success (True, False), value/error_message
    try:
        model_class = get_model_class_from_request(request)

        column_name = request.POST['column']
        value = request.POST['value'].strip()
        if is_foreign_key(column_name, model_class):
            # TODO: resolve foreign_key problem
            value = get_foreign_key(column_name, model_class, value)
            #   value = getattr(model_class, column_name).get_query_set()[0]

        obj = model_class.objects.filter(id=request.POST['row_id']).update(**{column_name: value})

        t = Transaction()
        t.author = request.POST.get('author', '')
        t.type = 'update_cell'

        t.model = request.POST['model']
        t.module = request.POST['module']

        t.rowId = request.POST['row_id']
        t.column = column_name
        t.originalValue = request.POST['value'].strip()
        t.value = str(value)

        t.save()

        response_data = {'success': True, 'value': str(value)}
    except Exception as e:
        response_data = {'success': False, 'error_message': str(e)}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@require_GET
def load_transactions(request):
    # ajax request
    # params: [module, model, last_transaction_id]
    module = request.GET['module']
    model = request.GET['model']
    last_transaction_id = request.GET['last_transaction_id']

    objs = Transaction.objects.\
        filter(module=module, model=model, type="update_cell").\
        filter(id__gt=last_transaction_id).order_by('id')
    response_data = [{
        "id": obj.id,
        "column": obj.column,
        "rowId": obj.rowId,
        "value": obj.value
    } for obj in objs]
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@require_POST
@csrf_exempt
def add_new_row(request):
    # ajax request
    # params: [module, model, data { column: value }]
    # return: success (True, False), error_message?
    try:
        data = json.loads(request.POST['data'])

        model_class = get_model_class_from_request(request)
        new_obj = model_class()

        #if unique_columns and len(model_class.objects.filter(**{column: request.POST[column] for column in unique_columns})) > 0:
        #    raise ValueError('Объект с такими ' + ' и '.join(unique_columns) + ' уже существует')

        for column_name in data:
            if is_foreign_key(column_name, model_class):
                value = get_foreign_key(column_name, model_class, data[column_name])
            else:
                value = get_field_value(column_name, model_class, data[column_name])
            setattr(new_obj, column_name, value)
        new_obj.save()

        t = Transaction()
        t.author = request.POST.get('author', '')
        t.type = 'add_row'

        t.module = request.POST['module']
        t.model = request.POST['model']

        t.rowId = new_obj.id
        t.value = request.POST['data']
        t.originalValue = request.POST['data']

        t.save()

        response_data = {'success': True}
    except Exception as e:
        response_data = {'success': False, 'error_message': str(e)}
    return HttpResponse(json.dumps(response_data), content_type='application/json')
