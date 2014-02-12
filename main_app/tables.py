# coding: utf-8

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
            'weight': 0.7,
        },
        'surname': {
            'autocomplete': True,
            'weight': 1.3,
        },
        'name': {
            'autocomplete': True,
            'weight': 0.9
        },
        'gender': {
            # TODO: enable
            # 'frontend_validation': '''function(row) {
            #                              gender = row.gender;
            #                              if (gender == "м" || gender == "ж") {
            #                               return true;
            #                              } else {
            #                               return false;
            #                              }
            #                          }''',
            'weight': 0.1,
            'default-value': 'м',
        },
        'school': {
            # TODO: can you implement it?
            # 'str': 'name_and_city',  # default representation is str(...)
            # inb4: too hard to implement

            'autocomplete': True,
            'weight': 2.5,
        },
        'grade': {
            'autocomplete': False,
            'weight': 0.1,
            'default_value': '6',
        }
    },
    'meta': {
        'add_new': True,
        'autoupdate': True,
        'model': Participant,
        'search': True,
        'sort_by': ('-id',),
        'column_ordering': ('test_number', 'surname', 'name', 'gender', 'school', 'grade'),
        'initial_focus': 'number',
        'focus_after_change': 'add_new',  # choices: add_new, search
        'focus_after_add': 'add_new',
        'search_by': ('number', 'surname', 'name', 'school'),
    }
}

SchoolsTableConfig = {
    'columns': {
        'name': {
            'weight': 0.5,
        },
        'city': {
            'weight': 0.8,
            'default_value': 'Москва'
        },
        'nominative': {
            'weight': 3,
        }
    },
    'meta': {
        'add_new': True,
        'autoupdate': True,
        'search': True,
        'model': School,
        'sort_by': ('city', 'name'),
        'column_ordering': ('name', 'city', 'nominative'),
        'initial_focus': 'name',
        'focus_after_change': 'none',
        'focus_after_add': 'add_new',
        'search_by': ('name', 'city', 'nominative')
    }
}

ResultsTableConfig = {
    'columns': {
        'number': {
        },
        'points_1': {
            'max_length': 1,
        },
        'points_2': {
            'max_length': 1,
        },
        'points_3': {
            'max_length': 1,
        },
        'points_4': {
            'max_length': 1,
        },
        'points_5': {
            'max_length': 1,
        },
        'points_6': {
            'quick_focus': False,
            'max_length': 1,
        },
        'sum': {
            'quick_focus': False,
            'frontend_validation': ''' function(row) {
                                            sum = +row.points_1 + +row.points_2 + +row.points_3 + +row.points_4 + +row.points_5 + +row.points_6;
                                            return row.sum == sum;
                                        }'''
        }
    },
    'meta': {
        'add_new': False,
        'search': True,
        'autoupdate': True,
        'model': Participant,
        'initial_focus': 'points_1',
        'search_by': ('number', 'name', 'surname'),
        'focus_after_change': 'search',
        'column_ordering': ('number', 'surname', 'name', 'points_1', 'points_2', 'points_3', 'points_4', 'points_5', 'points_6', 'sum'),
    }
}
