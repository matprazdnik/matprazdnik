#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import csv
import colorama
print(colorama.Style.BRIGHT)
                

def read_tuples_from_csv(csv_filename, name_map, namedtuple_class):
    fin = open(csv_filename, 'r', encoding='utf-8')
    table = csv.reader(fin, delimiter=',', )
    head = None
    tuples = []
    for linenumber, row in enumerate(table):
        if not head:
            head = row                
        else:
            if any(row):
                d = {}
                for i, value in enumerate(row):
                    try:
                        d[name_map[head[i]]] = value
                    except KeyError:
                        pass
            tuples.append(namedtuple_class(**d))
    return tuples


def dialog_choices(message, varieties):
    choice = dialog(message + '\n' + '\n'.join('{0}. {1}'.format(i, v) for i, v in enumerate(varieties, 1)))
    return varieties[0]
    return varieties[int(choice) - 1]


def dialog(message):
    print(message)
    print(">>>", end=' ') 
    sys.stdout.flush()
    res = input().strip()
    print()
    return res


def warning(s):
    print(colorama.Fore.YELLOW + s + colorama.Fore.RESET)


def error(s):
    print(colorama.Fore.RED + s + colorama.Fore.RESET)


def validate_number(number):
    return (int(number) % 19 == 0) or ((len(number) == 6) and (number.startswith('19') or number.startswith('38')))


def normalize_city(school):
    if school.city == '':
        school.city = 'Москва'
    if school.city.startswith('г. '):
        school.city = school.city[3:]
    elif school.city.startswith('г.'):
        school.city = school.city[2:]
    elif school.city.startswith('город '):
        school.city = school.city[6:]
    school.city = school.city[0].capitalize() + school.city[1:]
