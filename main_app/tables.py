 # coding: utf-8

from django.utils.safestring import mark_safe

from main_app.models import Participant, School

RegistrationTableConfig = {
    'columns': {
        'test_number': {
            # TODO: request rules from Raskin
            # 'frontend_validation': '''function(row) {
            #                              num = row.number;
            #                              if (num.length != 6) return false;
            #                              if ((+num[0] + +num[1] + +num[2] + +num[3]) % 10 != +num[4]) return false;
            #                              if ((+num[0] + 3*num[1] + 5*num[2] + 7*num[3]) % 10 != +num[5]) return false;
            #                              return true;
            #                          }''',
            'autocomplete': False,  # see http://jqueryui.com/autocomplete/
            'display_name': 'номер работы',
            'weight': 0.7,
        },
        'surname': {
            'autocomplete': True,
            'display_name': 'фамилия',
            'weight': 1.3,
        },
        'name': {
            'autocomplete': True,
            'display_name': 'имя',
            'weight': 0.9
        },
        'gender': {
            'frontend_validation': mark_safe('''function(row) {
                                        gender = row.gender;
                                        if (gender == "м" || gender == "ж") {
                                            return true;
                                        } else {
                                            return false;
                                        }
                                      }'''),
            'weight': 0.3,
            'display_name': 'пол',
            'default-value': 'м',
        },
        'school': {
            # TODO: can you implement it?
            # 'str': 'name_and_city',  # default representation is str(...)
            # inb4: too hard to implement
            'display_name': 'школа',
            'autocomplete': True,
            'weight': 2.5,
        },
        'grade': {
            'autocomplete': False,
            'display_name': 'класс',
            'weight': 0.3,
            'default_value': '6',
        }
    },
    'meta': {
        'table_name': 'registration',
        'add_new': True,
        'autoupdate': True,
        'model': Participant,
        'search': True,
        'sort_by': ('-id',),
        'column_ordering': ('test_number', 'surname', 'name', 'gender', 'school', 'grade'),
        'initial_focus': 'test_number',
        'focus_after_change': 'add_new',  # choices: add_new, search
        'focus_after_add': 'add_new',
        'search_by': ('test_number', 'surname', 'name', 'school'),
    }
}

SchoolsTableConfig = {
    'columns': {
        'nominative': {
            'display_name': 'краткое имя школы',
            'weight': 3,
        },
    },
    'meta': {
        'table_name': 'school',
        'add_new': True,
        'autoupdate': True,
        'search': True,
        'model': School,
        'sort_by': ('city', 'name'),
        'column_ordering': ('nominative', ),
        'initial_focus': 'name',
        'focus_after_change': 'none',
        'focus_after_add': 'none',
        'search_by': ('nominative', )
    }
}

ResultsTableConfig = {
    'columns': {
        'test_number': {
            'display_name': 'номер работы',
        },
        'points_1': {
            'display_name': '1',
            'max_length': 1,
        },
        'points_2a': {
            'display_name': '2a',
            'max_length': 1,
        },
        'points_2b': {
            'display_name': '2b',
            'max_length': 1,
        },
        'points_3': {
            'display_name': '3',
            'max_length': 1,
        },
        'points_4': {
            'display_name': '4',
            'max_length': 1,
        },
        'points_5': {
            'display_name': '5',
            'max_length': 1,
        },
        'points_6': {
            'display_name': '6',
            'quick_focus': False,
            'max_length': 1,
        },
        'sum': {
            'display_name': 'сумма',
            'quick_focus': False,
            'frontend_validation': ''' function(row) {
                                            sum = +row.points_1 + +row.points_2a + +row.points_2b + +row.points_3 + +row.points_4 + +row.points_5 + +row.points_6;
                                            return row.sum == sum;
                                        }'''
        }
    },
    'meta': {
        'table_name': 'results',
        'add_new': False,
        'search': True,
        'autoupdate': True,
        'model': Participant,
        'initial_focus': 'points_1',
        'search_by': ('test_number', 'name', 'surname'),
        'focus_after_change': 'search',
        'column_ordering': ('test_number', 'points_1', 'points_2a', 'points_2b', 'points_3', 'points_4', 'points_5', 'points_6', 'sum'),
    }
}
