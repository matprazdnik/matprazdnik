#!/usr/bin/env python

import sys
import csv

from main_app.models import School

def main():
    if len(sys.argv) != 2:
        print("Usage", sys.argv[0], "<path_to_new_file>")
        sys.exit(1)
    export_file = open(sys.argv[1], "w", encoding="utf-8")
    exporter = csv.writer(export_file, delimiter="\t")
    exporter.writerow(['Код СтатГрад', 'Полное название', 'Красивое название'])

    schools = School.objects.all()
    cnt_schools = 0
    for school_obj in schools:
        exporter.writerow([getattr(school_obj, 'statgrad_code'),
                           getattr(school_obj, 'official_name'),
                           getattr(school_obj, 'nominative')])
        cnt_schools += 1

    print("Exported", cnt_schools, "schools to", sys.argv[1])

if __name__ == '__main__':
    main()
