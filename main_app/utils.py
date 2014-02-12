# coding: utf-8


def genitive(word):
    if word[-1] == 'о':
        return word[:-1] + 'о'
    elif word[-1] == 'а':
        return word[:-1] + 'ы' if word[-2] not in 'гкх' else word[:-1] + 'и'
    elif word[-1] in ('ы', 'и', 'й'):
        return word
    elif word[-2:] == 'ый':
        return word[-2:] + 'ого'
    else:
        return word + 'а'


def get_school_genitive(name, city):
    return 'школы №{0} г. {1}'.format(name, genitive(city))


def normalize_city(city):
    if city.startswith('г. '):
        city = city[3:]
    elif city.startswith('г.'):
        city = city[2:]
    elif city.startswith('город '):
        city = city[6:]
    return city.capitalize()


def get_diploma_text(gender, grade, genitive):
    return 'учени{0} {1} класса {2}'.format('ка' if gender == 'm' else 'цы', grade, genitive)


def get_degree(sum):
    return 'бознать какой степени'
