from django.core.management.base import BaseCommand
from optparse import make_option
from libguide.models import Library
import sys
import csv

class Command(BaseCommand):
    help = "Load Library Models from csv - RUN ME FIRST"

    option_list = BaseCommand.option_list + (
        make_option('--verbose', dest='verbose', default=False, help='Verbose mode'),
        make_option('--delimiter', dest='delimiter', default=',', help='CSV file delimiter'),
        make_option('--quotechar', dest='quotechar', default='"', help='CSV file quote character'),
    )

    _primary_field = 'name'

    # dictionary keys are CSV column headings, values are model field names
    _field_map = {
        'Library name': 'name',
        'Library URL': 'url',
        'Library description': 'description'
    }

    def handle(self, *args, **options):

        if options['verbose']:
            print >> sys.stderr, "delimiter is '{0}'".format(options['delimiter'])
            print >> sys.stderr, "quote character is '{0}'".format(options['quotechar'])

        data = []
        if len(args) and args[0][1] != '-':
            with open(args[0], 'r') as f:
                for row in csv.reader(f, delimiter=options['delimiter'], quotechar=options['quotechar']):
                    try:
                        if len(data) == 0:
                            if len(row) != len(self._field_map):
                                print >> sys.stderr, "Field count mismatch: {0} fields, {1} "
                                sys.exit(1)

                            for label in row:
                                label = label.strip()

                                if options['verbose']:
                                    print >> sys.stderr, "field: '{0}' = {1}".format(label, self._field_map[label])

                                data.append({'field': self._field_map[label]})

                        else:
                            library = {}
                            for i in range(len(data)):
                                library[data[i]["field"]] = row[i]

                            try:
                                prime = { self._primary_field: library[self._primary_field] }

                                lib = Library.objects.get(**prime)

                                if options['verbose']:
                                    print >> sys.stderr, "FOUND {0}".format(prime)

                                for (k, v) in library.items():
                                    setattr(lib, k, v)

                            except Library.DoesNotExist as err:
                                print >> sys.stderr, "NOT FOUND {0}".format(library[self._primary_field])
                                lib = Library(**library)

                            lib.save()


                    except KeyError as err:
                        print >> sys.stderr, "label '{0}' not in model".format(label)
                        sys.exit(1)
