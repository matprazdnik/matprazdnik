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
    mapped_model_class = field.related.parent_model;
    objects = list(mapped_model_class.objects.all())
    equal_objects = list(filter(lambda object: str(object) == value, objects))
    like_objects = list(filter(lambda object: value in str(object), objects))
    if len(equal_objects) == 1:
        return equal_objects[0]
    if len(like_objects) > 1:
        raise KeyError("Неоднозначность");
    elif len(like_objects) == 0:
        raise KeyError("Нет таких")
    else:
        return like_objects[0]

def convert_value_to_field_type(s, django_field_type):
    if isinstance(django_field_type, IntegerField):
        return int(s)
    elif isinstance(django_field_type, CharField):
        return s
    else:
        raise NotImplementedError(str(django_field_type) + ' not supported yet')