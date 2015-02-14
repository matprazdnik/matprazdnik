import csv
import sys

from main_app.models import School, Participant


GENDERS = {'м', 'ж'}

PARTICIPANT_FIELDS_NAME_MAP = {
    'Код версии': 'version_code',
    'Код участника': 'participant_code',
    'Код анкеты': 'poll_code',
    'Фамилия': 'surname',
    'Имя': 'name',
    'Класс': 'grade',
    'Пол': 'gender',
    'Короткое название школы': 'nominative',
}


def read_rows_from_csv(csv_filename, name_map):
    fin = open(csv_filename, 'r', encoding='utf-8')
    table = csv.reader(fin, delimiter=',')
    head = None
    rows = []
    for row in table:
        if not head:
            head = row
        else:
            if any(row):
                d = {}
                for i, value in enumerate(row):
                    if head[i] in name_map:
                        d[name_map[head[i]]] = value.strip()
                rows.append(d)
    return rows


def check_unique(rows, key):
    '''
    >>> check_unique([{'a': 1, 'b': 10}, {'a': 2, 'b': 10}], 'a')
    True
    >>> check_unique([{'a': 1, 'b': 10}, {'a': 2, 'b': 10}], 'b')
    False
    '''
    return len({row[key] for row in rows}) == len(rows)


def preprocess_db(participants):
    check_unique(participants, 'version_code')
    check_unique(participants, 'participant_code')
    check_unique(participants, 'poll_code')

    for participant in participants:
        try:
            assert participant['version_code']
            assert participant['participant_code']
            assert participant['poll_code']
            assert participant['surname']
            assert participant['name']
            assert int(participant['grade'])
            assert participant['gender'] in GENDERS
            assert participant['nominative']

            participant['surname'] = participant['surname'].title()
            participant['name'] = participant['name'].title()
        except Exception as e:
            raise ValueError(participant) from e


def update_schools(participants):
    for participant in participants:
        nominative = participant['nominative']
        if not School.objects.filter(nominative=nominative):
            School(nominative=nominative).save()
            print('School created: {0}'.format(nominative))
        else:
            print('School already found: {0}'.format(nominative))


def update_participants(participants):
    for participant in participants:
        participant_tuple = participant['version_code'], participant['name'], participant['surname']
        if not Participant.objects.filter(version_code=participant['version_code']):
            school = School.objects.get(nominative=participant['nominative'])
            Participant(version_code=participant['version_code'],
                        participant_code=participant['participant_code'],
                        poll_code=participant['poll_code'],
                        surname=participant['surname'],
                        name=participant['name'],
                        gender=participant['gender'],
                        grade=participant['grade'],
                        school=school).save()
            print('Participant created: {0} {1} {2}'.format(*participant_tuple))
        else:
            print('Participant already found: {0} {1} {2}'.format(*participant_tuple))


def main():
    if len(sys.argv) != 2:
        print('Usage: {0} REGISTRATION_DB.csv'.format(sys.argv[0]))
        sys.exit(1)
    else:
        REGISTRATION_DB_FILENAME = sys.argv[1]
        participants = read_rows_from_csv(REGISTRATION_DB_FILENAME, PARTICIPANT_FIELDS_NAME_MAP)
        participants = [participant
                        for participant in participants
                        if int(participant['grade']) < 7]
        preprocess_db(participants)
        update_schools(participants)
        update_participants(participants)


if __name__ == '__main__':
    main()
