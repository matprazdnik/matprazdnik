# -*- coding: utf-8 -*-


import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .utils import (is_foreign_key, get_field_by_name, get_field_value,
                    get_foreign_key, get_model_class, convert_value_to_string,
                    join_obj_fields)


NEW_ROWS_CHUNK_SIZE = 50


@require_GET
def load_new_rows(request):
    # ajax request
    # params: [module, model, highest_loaded_id, columns_space_delimited]
    # return: {object id: object column values}
    highest_loaded_id = request.GET['highest_loaded_id']
    column_ordering = request.GET['columns_space_delimited'].split() + ['id']
    model_class = get_model_class(request)

    objs = model_class.objects.filter(id__gt=highest_loaded_id).order_by('id')[:NEW_ROWS_CHUNK_SIZE]
    response_data = {}
    for obj in objs:
        response_data[obj.id] = {}
        for column in column_ordering:
            response_data[obj.id][column] = convert_value_to_string(getattr(obj, column))
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@require_GET
def load_autocomplete_choices(request):
    # ajax request
    # params: [module, model, columns_space_delimited]
    # returns: {column_name: array of possible values}
    model_class = get_model_class(request)
    column_names = request.GET['columns_space_delimited'].split()
    response_data = {}
    for column_name in column_names:
        response_data[column_name] = []
        if is_foreign_key(column_name, model_class):
            foreign_key_model_class = get_field_by_name(column_name, model_class).related.parent_model
            response_data[column_name] = list(set([str(i) for i in foreign_key_model_class.objects.all()]))
        else:
            response_data[column_name] = list(set([str(getattr(i, column_name)) for i in model_class.objects.all()]))
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@require_GET
def get_search_hints(request):
    # ajax request
    # params: [module, model, search_fields_space_delimited]
    # return: [search_hints]
    model_class = get_model_class(request)
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
    model_class = get_model_class(request)
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
    # params: [row_id, field_name, new_field_value, module, model]
    # return: success (True, False), value/error_message
    try:
        model_class = get_model_class(request)
        obj = model_class.objects.get(id=request.POST['row_id'])
        column_name = request.POST['field_name']
        value = request.POST['new_field_value'].strip()
        if column_name.startswith('points') and not value:
            value = 0
        if is_foreign_key(column_name, model_class):
            # TODO: resolve foreign_key problem
            value = get_foreign_key(column_name, model_class, value)
            #   value = getattr(model_class, column_name).get_query_set()[0]
        setattr(obj, column_name, value)
        obj.save()
        # TODO: maybe pass module, model, row_id to response?
        response_data = {'success': True, 'value': str(value)}
    except Exception as e:
        response_data = {'success': False, 'error_message': str(e)}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@require_POST
@csrf_exempt
def add_new_row(request):
    # ajax request
    # params: [module, model, columns_space_delimited, unique_columns]
    # return: success (True, False), error_message?
    try:
        column_ordering = request.POST['columns_space_delimited'].split()
        model_class = get_model_class(request)
        new_obj = model_class()

        unique_columns = request.POST['unique_columns'].split()

        if unique_columns and len(model_class.objects.filter(**{column: request.POST[column] for column in unique_columns})) > 0:
            raise ValueError('Объект с такими ' + ' и '.join(unique_columns) + ' уже существует')

        for column_name in column_ordering:
            if is_foreign_key(column_name, model_class):
                # TODO: resolve foreign_key problem
                value = get_foreign_key(column_name, model_class, request.POST[column_name])
                # value = getattr(model_class, column_name).get_query_set()[0]
            else:
                value = get_field_value(column_name, model_class, request.POST[column_name])
            setattr(new_obj, column_name, value)
        new_obj.save()
        response_data = {'success': True}
    except Exception as e:
        response_data = {'success': False, 'error_message': str(e)}
    return HttpResponse(json.dumps(response_data), content_type='application/json')
