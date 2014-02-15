#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import pickle
import urllib.request
import json
import pprint

from collections import namedtuple
from my_utils import read_tuples_from_csv, dialog, dialog_choices


school_fields_name_map = {
	'Номер школы': 'number',
	'Статус школы': 'type',
	'Город школы': 'city',
	'Короткое название школы': 'nominative'
}

participant_fields_name_map = dict({
	'Код версии': 'version',
	'Код участника': 'code',
	'Фамилия': 'surname',
	'Имя': 'name',
	'Класс': 'grade',
	'Номер школы': 'number',
	'Город школы': 'city',
	'Короткое название школы': 'nominative'
}, **school_fields_name_map)

School = namedtuple('School', school_fields_name_map.values())
Participant = namedtuple('Participant', participant_fields_name_map.values())

class FileDict():
	def __init__(self, filename):
		self.filename = filename
		try:
			input_ = open(filename, 'rb')
			self.d = pickle.load(input_)
			input_.close()
		except (FileNotFoundError, EOFError):
			self.d = {}

	def save(self):
		output = open(self.filename, 'wb')
		pickle.dump(self.d, output)
		output.close()

	def __getitem__(self, key):
		return self.d[key]

	def __setitem__(self, key, value):
		self.d[key] = value
		self.save()

	def __contains__(self, key):
		return key in self.d


strange_cities = FileDict('strange_cities.pickle')


def clean_school_name(s):
	bad_substrings = ['Государственноебюджетное образовательное учреждение', ''
	]
	s = s.replace('ГБОУ', '')
	s = s.replace('Лицей', 'лицей')
	s = ' '.join(s.split())
	return s


def extract_city(raw_city):
	raw_city = raw_city.strip()
	if not raw_city or raw_city == '0' or 'Москва' in raw_city:
		raw_city = 'Москва'
	regexps = ['(?:[Гг]ород |[Гг]\.(?![Оо]\.)\s?)(\w+)',
			   '^(\w+)$',
			   '(?:[Рр]оссия|[Уу]краина)[,\s]*(\w+)(?! обл)',
			   '(\w+)(?! область)[,\s]*(?:[Рр]оссия|[Уу]краина)'
			  ]
	for regexp in regexps:
		mo = re.search(regexp, raw_city, flags=re.UNICODE)
		if mo:
			city = mo.groups()[0].capitalize()
			print('\t', raw_city, ':\t\t' + city)
			return city
	else:
		if raw_city not in strange_cities:
			strange_cities[raw_city] = dialog('Что это за город: ' + raw_city + '?')
		return strange_cities[raw_city]


def get_city(school):
	return ('г. ' if re.match('^(?:\w|-)+', school.city) else '') + school.city


def get_default_school_name(school):
	return '{0} №{1}, {2}'.format(school.type, school.number, get_city(school))


def normalize_school_name(name):
	name = name.replace('<<', '«').replace('>>', '»')
	name = re.sub(r' "', ' «', name)
	name = re.sub(r'" ', '» ', name)
	name = re.sub(r'"$', '»', name)
	return name


def generate_school_db():
	schools = read_tuples_from_csv(sys.argv[2], school_fields_name_map, School)
	
	for i, school in enumerate(schools):
		schools[i] = school._replace(city = extract_city(school.city))

	added_schools = FileDict('added_schools.pickle')

	for school in schools:
		name = school.number if school.number else school.nominative
		if False: # (name, school.city) in added_schools:
			continue
		# same_schools = [s2 for s2 in schools if s2.number == school.number and s2.city == school.city]
		# choices = list(sorted(set(clean_school_name(s3)
			    # for s3 in [get_default_school_name(s2) for s2 in same_schools] + [s2.nominative for s2 in same_schools])))
		# chosen_name = dialog_choices('Выберите название для школы ' + str(school), choices)
		
		# Использовалось в 2013 году
		# try:
		# 	int(school.number)
		# 	chosen_name = get_default_school_name(school)
		# except ValueError:
		# 	chosen_name = normalize_school_name(school.nominative) + ', ' + get_city(school)

		# В 2014 году Миша Раскин ввёл волшебное поле "Короткое название школы"
		chosen_name = normalize_school_name(school.nominative)

		added_schools[(name, school.city)] = chosen_name
		print(name, school.city, chosen_name, sep='\t')

		for i in range(2):
			try:
				request = urllib.request.Request('http://' + IP_PORT + '/flying_rows/add_new_row/')
				data = urllib.parse.urlencode({'module': 'main_app.models',
						'model': 'School',
						'columns_space_delimited': 'name city nominative',
						'name': name,
						'city': school.city,
						'nominative': chosen_name,
						'unique_columns': 'name city',
				}).encode('utf8')
			except ConnectionResetError as e:
				print(str(e))
				continue

		print(json.loads(urllib.request.urlopen(request, data=data).read().decode('utf8')))

		added_schools.save()


def add_participants():
	participants = read_tuples_from_csv(sys.argv[2], participant_fields_name_map, Participant)
	versions_by_code = {}

	for p in participants:
		if p.code not in versions_by_code or p.code in versions_by_code and int(p.version) > int(versions_by_code[p.code].version):
			versions_by_code[p.code] = p

	def guess_gender(name):
		return 'ж' if name[-1] in 'аяь' and name[-1] != 'Никита' else 'м'

	for version in versions_by_code:
		p = versions_by_code[version]

		if p.grade == '7':
			continue

		p = p._replace(surname = p.surname.capitalize(), name = p.name.capitalize())

		# print(p)

		for i in range(2):
			try:
				request = urllib.request.Request('http://' + IP_PORT + '/flying_rows/add_new_row/')
				data = urllib.parse.urlencode({'module': 'main_app.models',
						'model': 'Participant',
						'columns_space_delimited': 'version_code participant_code surname name gender grade school',
						'version_code': p.version,
						'participant_code': p.code,
						'surname': p.surname,
						'name': p.name,
						'gender': guess_gender(p.name),
						'grade': p.grade,
						'school': normalize_school_name(p.number if p.number else p.nominative) + ' ' + extract_city(p.city),
						'unique_columns': 'surname name',
				}).encode('utf8')

				message = json.loads(urllib.request.urlopen(request, data=data).read().decode('utf8'))
				if not message['success'] and not message['error_message'].startswith('Объект'):
					print(message)
				break
			except ConnectionResetError as e:
				print(str(e))
				continue


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: generate_school_db.py IP:PORT REGISTER_DB.csv')
		sys.exit(1)
	else:
		IP_PORT = sys.argv[1]
		generate_school_db()
		add_participants()
		# strange_cities.save()