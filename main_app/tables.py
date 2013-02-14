# coding: utf-8

from main_app.models import Participant, School
from main_app.utils import get_school_genitive, normalize_city, get_diploma_text, get_degree

RegistrationTableConfig = {
    'columns': {
        'number': {
            'frontend_validation': '''function validate(num) {
                                          return ((+num[0] + +num[1] + +num[2] + +num[3]) % 10 == +num[4]) && ((+num[0] + 3*num[1] + 5*num[2] + 7*num[3]) % 10 == +num[5]);
                                      }''',
            'search_hint': False,  # see http://jqueryui.com/autocomplete/
            'weight': 0.7,
        },
        'surname': {
            'search_hint': False,
            'weight': 1.5,
        },
        'name': {
            'search_hint': True,
        },
        'gender': {
            'weight': 0.1,
        },
        'school': {
#            'str': 'name_and_city',  # default representation is str(...)
            # too hard to implement
            'search_hint': True,
            'weight': 2.5,
        },
        'grade': {
            'search_hint': False,
            'weight': 0.1,
        }
    },
    'meta': {
        'add-new': True,
        'model': Participant,
        'sort_by': ('-id',),
        'column_ordering': ( 'number', 'surname', 'name', 'gender', 'school', 'grade'),
        'initial_focus': 'number',
        'after_save_focus': 'add_new',  # choices: add_new, search
        'search_by': ('number', 'surname', 'school'),
        'update-url': 'participants/update/', # TODO: update with relative path
        'add-url': 'participants/add/',
        'get-new-url': 'participants/getnew/'
    }
}

#class SchoolsTable(django_tables2.table):
#    name': )
#    city': backend_normalize=normalize_city)
#    genitive': backend_auto_generated=(lambda row: get_school_genitive(row.name, row.city)))
#
#    class Meta:
#        model': School
#        sort_by': ('city', 'name')
#        sequence': ('name', 'city', 'genitive')
#        initial_focus': 'name'
#        after_save_focus': 'search'
#        search_by': ('name', 'city', 'genitive')
#
#
#class PointsTable(django_tables2.table):
#    number': backend_validation=(lambda row: int(row.number) % 19 == 0))
#    surname': search_hint=False)
#    name': search_hint=True)
#    points_1': default=0)
#    points_2': default=0)
#    points_3': default=0)
#    points_4': default=0)
#    points_5': default=0)
#    points_6a': default=0)
#    points_6b': default=0)
#    manual_sum': django_tables2.GhostColumn(backend_validation=
#            (lambda row: row.manual_sum == row.sum),
#            validation_error='ручная сумма не совпадает с автосуммой')
#    sum': backend_formula=
#            (lambda row: row.points_1 + row.points_2 + row.points_3 + row.points_4 +
#                         row.points_5 + row.points_6a + row.points_6b))
#    # GhostColumn is one that is absent in model and won't be saved into database
#    # the difference between formula and auto_generated is that you can't change the field with formula
#    # auto_generated is generated only once
#
#    class Meta:
#        model': Participant
#        sort_by': ('surname', 'name')
#        sequence': ('number', 'surname', 'name', 'points_1', 'points_2', 'points_3',
#                    'points_4', 'points_5', 'points_6a', 'points_6b', 'manual_sum', 'auto_sum')
#        initial_focus': 'points_1'
#        after_save_focus': 'search'
#        search_by': ('number', 'surname')
#
#
#class DiplomasTable(django_tables2.table):
#    surname': )
#    name': )
#    grade': )
#    school': str='name_and_city')
#    diploma_text': django_tables2.GhostColumn(backend_formula=
#            (lambda row: get_diploma_text(row.gender, row.grade, row.school.genitive)))
#    sum': )
#    degree': django_tables2.GhostColumn(backend_formula=(lambda row: get_degree(row.sum)))
#
#    class Meta:
#        model': Participant
#        sort_by': ('-sum', 'surname', 'name')
#        sequence': ('surname', 'name', 'grade', 'school', 'diploma_text', 'sum', 'degree')
#        initial_focus': ('surname')
#        after_save_focus': 'search'
#        enable_add_new': False  # default is True for both enable_add_new and enable_search
#        search_by': ('surname', 'school', 'degree')