import django_tables2
from main_app.models import Participant, School
from main_app.utils import get_school_genitive, normalize_city, get_diploma_text, get_degree


class RegistrationTable(django_tables2.table):
    number = django_tables2.Column(backend_validation=(lambda row: int(row.number) % 19 == 0), search_hint=False)
                                # I want to implement frontend validation as well (via JavaScript function)
    surname = django_tables2.Column(search_hint=False)
    name = django_tables2.Column(search_hint=True)
    gender = django_tables2.Column()  # no search_hint, because it's a choice field. see comment below
    school = django_tables2.Column(str='name_and_city', search_hint=True)  # default representation is str(...)
    grade = django_tables2.Column(search_hint=False)

    class Meta:
        model = Participant  # used to predict column type. eg.: gender is a choice field and should be
                             # drawn with select or radio-buttons (how exactly?)
        sort_by = ('-id',)
        sequence = ('id', 'number', 'surname', 'name', 'gender', 'school', 'grade')
        initial_focus = 'number'
        after_save_focus = 'add_new'  # choices: add_new, search
        search_by = ('number', 'surname', 'school')


class SchoolsTable(django_tables2.table):
    name = django_tables2.Column()
    city = django_tables2.Column(backend_normalize=normalize_city)
    genitive = django_tables2.Column(backend_auto_generated=(lambda row: get_school_genitive(row.name, row.city)))

    class Meta:
        model = School
        sort_by = ('city', 'name')
        sequence = ('name', 'city', 'genitive')
        initial_focus = 'name'
        after_save_focus = 'search'
        search_by = ('name', 'city', 'genitive')


class PointsTable(django_tables2.table):
    number = django_tables2.Column(backend_validation=(lambda row: int(row.number) % 19 == 0))
    surname = django_tables2.Column(search_hint=False)
    name = django_tables2.Column(search_hint=True)
    points_1 = django_tables2.Column(default=0)
    points_2 = django_tables2.Column(default=0)
    points_3 = django_tables2.Column(default=0)
    points_4 = django_tables2.Column(default=0)
    points_5 = django_tables2.Column(default=0)
    points_6a = django_tables2.Column(default=0)
    points_6b = django_tables2.Column(default=0)
    manual_sum = django_tables2.GhostColumn(backend_validation=
            (lambda row: row.manual_sum == row.sum),
            validation_error='ручная сумма не совпадает с автосуммой')
    sum = django_tables2.Column(backend_formula=
            (lambda row: row.points_1 + row.points_2 + row.points_3 + row.points_4 +
                         row.points_5 + row.points_6a + row.points_6b))
    # GhostColumn is one that is absent in model and won't be saved into database
    # the difference between formula and auto_generated is that you can't change the field with formula
    # auto_generated is generated only once

    class Meta:
        model = Participant
        sort_by = ('surname', 'name')
        sequence = ('number', 'surname', 'name', 'points_1', 'points_2', 'points_3',
                    'points_4', 'points_5', 'points_6a', 'points_6b', 'manual_sum', 'auto_sum')
        initial_focus = 'points_1'
        after_save_focus = 'search'
        search_by = ('number', 'surname')


class DiplomasTable(django_tables2.table):
    surname = django_tables2.Column()
    name = django_tables2.Column()
    grade = django_tables2.Column()
    school = django_tables2.Column(str='name_and_city')
    diploma_text = django_tables2.GhostColumn(backend_formula=
            (lambda row: get_diploma_text(row.gender, row.grade, row.school.genitive)))
    sum = django_tables2.Column()
    degree = django_tables2.GhostColumn(backend_formula=(lambda row: get_degree(row.sum)))

    class Meta:
        model = Participant
        sort_by = ('-sum', 'surname', 'name')
        sequence = ('surname', 'name', 'grade', 'school', 'diploma_text', 'sum', 'degree')
        initial_focus = ('surname')
        after_save_focus = 'search'
        enable_add_new = False  # default is True for both enable_add_new and enable_search
        search_by = ('surname', 'school', 'degree')