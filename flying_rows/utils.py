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


def convert_value_to_field_type(s, django_field_type):
    if isinstance(django_field_type, IntegerField):
        return int(s)
    elif isinstance(django_field_type, CharField):
        return s
    else:
        raise NotImplementedError(str(django_field_type) + ' not supported yet')