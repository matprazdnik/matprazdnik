import csv
import sys

from main_app.models import School, Participant

SKIPPED_PARICIPANTS = 0
DOUBLED_PARTICIPANTS = 0
NOT_MOSCOW_PARTICIPANTS = 0

GENDERS = {'м', 'ж'}

PARTICIPANT_FIELDS_NAME_MAP = {
    'код версии': 'version_code',
    'Код (не менять)': 'participant_code',
    'Фамилия*': 'surname',
    'Имя*': 'name',
    'Класс, в котором Вы учитесь': 'grade',
    'Пол*': 'gender',
    'Краткое название школы': 'nominative',
    'Логин школы в системе СтатГрад*': 'school_code'
}

SCHOOL_FIELDS_NAME_MAP = {
    'Код СтатГрад': "code",
    'Полное название': "full_name",
    'Красивое название': "nominative"
}

def read_rows_from_csv(csv_filename, name_map):
    fin = open(csv_filename, 'r', encoding='utf-8')
    table = csv.reader(fin, delimiter='\t')
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

    for participant in participants:
        try:
            assert participant['version_code']
            assert participant['participant_code']
            assert participant['surname']
            assert participant['name']
            assert int(participant['grade'])
            assert participant['gender'] in GENDERS
            #assert participant['nominative']
            #assert participant['school_code']

            participant['surname'] = participant['surname'].title()
            participant['name'] = participant['name'].title()
        except Exception as e:
            raise ValueError(participant) from e


def update_schools(schools):
    for school in schools:
        School(statgrad_code=school['code'],
               nominative=school['nominative'],
               official_name=school['full_name']).save()


def remove_existing_participants(participants):
    result = []
    for participant in participants:
        participant_tuple = (
            participant['participant_code'], participant['name'], participant['surname'])
        if not Participant.objects.filter(participant_code=participant['participant_code']):
            result.append(participant)
            # print('New participant: {0} {1} {2}'.format(*participant_tuple))
        else:
            pass
            # print('Participant found and removed: {0} {1} {2}'.format(*participant_tuple))
    return result


def update_participants(participants):
    SKIPPED_PARICIPANTS = 0
    DOUBLED_PARTICIPANTS = 0
    NOT_MOSCOW_PARTICIPANTS = 0
    for participant in participants:
        participant_tuple = (
            participant['participant_code'], participant['name'], participant['surname'])
        if not Participant.objects.filter(participant_code=participant['participant_code']):
            print('Try to find school:', participant['school_code'], participant['nominative'])
            if participant['school_code'] == "":
                print("Skip")
                SKIPPED_PARICIPANTS += 1
                continue
            schools = School.objects.filter(statgrad_code=participant['school_code'])
            if len(schools) > 1:
                print(schools)
            elif len(schools) == 0:
                print("No school found -", participant['school_code'], participant['nominative'])
                print("   ...participant skipped, add school first.")
                SKIPPED_PARICIPANTS += 1
                NOT_MOSCOW_PARTICIPANTS += 1
            else:
                school = schools[0]
                Participant(version_code=participant['version_code'],
                            participant_code=participant['participant_code'],
                            surname=participant['surname'],
                            name=participant['name'],
                            gender=participant['gender'],
                            grade=participant['grade'],
                            school=school).save()
                print('Participant created: {0} {1} {2}'.format(*participant_tuple))
        else:
            print('Participant already found: {0} {1} {2}'.format(*participant_tuple))
            DOUBLED_PARTICIPANTS += 1
    print("Participants skipped:", SKIPPED_PARICIPANTS, "out of", len(participants) - DOUBLED_PARTICIPANTS)
    print("                     ", NOT_MOSCOW_PARTICIPANTS, "are not from Moscow")

def main():
    if len(sys.argv) != 3:
        print('Usage: {0} [REGISTRATION_DB.csv|SCHOOL_LIST.csv] [-participants|-schools]'.format(sys.argv[0]))
        sys.exit(1)
    elif sys.argv[2] == '-participants':
        REGISTRATION_DB_FILENAME = sys.argv[1]
        participants = read_rows_from_csv(REGISTRATION_DB_FILENAME, PARTICIPANT_FIELDS_NAME_MAP)
        participants = [participant
                        for participant in participants
                        if participant['grade'] in ['1', '2', '3', '4', '5', '6']]
        participants = remove_existing_participants(participants)
        preprocess_db(participants)
        print("New participants:", len(participants))
        update_participants(participants)
    elif sys.argv[2] == '-schools':
        SCHOOL_LIST_FILENAME = sys.argv[1]
        schools = read_rows_from_csv(SCHOOL_LIST_FILENAME, SCHOOL_FIELDS_NAME_MAP)
        print("Schools to add:", len(schools))
        update_schools(schools)

    else:
        print('Usage: {0} [REGISTRATION_DB.csv|SCHOOL_LIST.csv] [-participants|-schools]'.format(sys.argv[0]))
        sys.exit(1)


if __name__ == '__main__':
    main()
