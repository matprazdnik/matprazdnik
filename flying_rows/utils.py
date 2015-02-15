import importlib

from django.db.models.fields.related import ForeignKey
from django.db.models.fields import IntegerField, CharField


def get_field_by_name(column_name, model_class):
    for field in model_class._meta.fields:
        if field.name == column_name:
            return field
    else:
        raise KeyError(column_name + ' not found among ' + model_class.__name__ + ' fields')


def is_foreign_key(column_name, model_class):
    return isinstance(get_field_by_name(column_name, model_class), ForeignKey)


def get_foreign_key(column_name, model_class, value):
    field = get_field_by_name(column_name, model_class)
    mapped_model_class = field.related.parent_model
    objects = list(mapped_model_class.objects.filter(deleted=False))
    equal_objects = list(filter(lambda object: str(object) == value, objects))

    def almost_like(obj):
        #WORKAROUND!
        try:
            columns = ['name', 'city', 'nominative']
            field_values = [getattr(obj, column) for column in columns]
            return all(chunk in field_values for chunk in value.split())
        except:
            return []

    almost_like_objects = list(filter(almost_like, objects))
    like_objects = list(filter(lambda object: all(chunk in str(object) for chunk in value.split()), objects))
    if len(equal_objects) == 1:
        return equal_objects[0]
    if len(almost_like_objects) == 1:
        return almost_like_objects[0]
    if len(like_objects) > 1:
        raise KeyError("Неоднозначность: Есть более двух объектов типа " + mapped_model_class._meta.verbose_name + ', соответствующих значению"' + value + '"')
    elif len(like_objects) == 0:
        raise KeyError("Нет объектов типа " + mapped_model_class._meta.verbose_name + ", соответствующих значению " + value)
    else:
        return like_objects[0]


def get_field_value(column_name, model_class, value):
    field = get_field_by_name(column_name, model_class)
    if value == '':
        try:
            value = field._meta.default_value
        except:
            pass
    return value


def convert_value_to_field_type(s, django_field_type):
    if isinstance(django_field_type, IntegerField):
        return int(s)
    elif isinstance(django_field_type, CharField):
        return s
    else:
        raise NotImplementedError(str(django_field_type) + ' not supported yet')

def get_model_class(module_name, model_name):
    module = importlib.import_module(module_name)
    return getattr(module, model_name)

def get_model_class_from_request(request):
    method = request.method
    module_name = getattr(request, method)['module']
    model_name = getattr(request, method)['model']
    return get_model_class(module_name, model_name)

def convert_to_string(x):
    if isinstance(x, list):
        return [convert_to_string(y) for y in x]
    if isinstance(x, dict):
        return {convert_to_string(k): convert_to_string(v) for (k, v) in x.items()}
    if x is None:
        return ''
    return str(x)


def join_obj_fields(obj, fields):
    return ' '.join([str(getattr(obj, field)) for field in fields])


def unique(iterable):
    return list(set(iterable))


def autocomplete_choices(column_name, model_class):
    if is_foreign_key(column_name, model_class):
        foreign_key_model_class = get_field_by_name(column_name, model_class).related.parent_model
        return unique(str(i) for i in foreign_key_model_class.objects.filter(deleted=False))
    else:
        return unique(str(getattr(i, column_name))
                      for i in model_class.objects.filter(deleted=False))


def get_table_data(table_config):
    model_class = table_config['meta']['model']
    objects = list(model_class.objects.filter(deleted=False))

    def get_necessary_data(object):
        return {column: getattr(object, column) for column in table_config['columns']}

    return convert_to_string({
        'rows': list(reversed([str(object.id) for object in objects])),
        'data': {str(object.id): get_necessary_data(object) for object in objects}
    })

