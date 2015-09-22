from django.core.management.base import BaseCommand
from optparse import make_option
from libguide.models import Library, Librarian, SubjectGuide
import sys
import csv

class Command(BaseCommand):
    help = "Load Librarian Models from csv"

    option_list = BaseCommand.option_list + (
        make_option('--verbose', dest='verbose', default=False, help='Verbose mode'),
        make_option('--delimiter', dest='delimiter', default=',', help='CSV file delimiter'),
        make_option('--quotechar', dest='quotechar', default='"', help='CSV file quote character'),
    )

    # primary model reference field
    _guide_key = 'name'
    _librarian_key = 'name'
    _library_key = 'name'

    # dictionary keys are CSV column headings, values are model field names
    _guide_map = {
        'Static Subject Guide Name': 'name',
        'Subject guide URL': 'url',
        'Subject guide link text': 'label'
    }

    _librarian_map = {
        'Librarian name': 'name',
        'Librarian email': 'email',
        'Librarian phone number': 'phone',
        'URL to librarian profile': 'url'
    }

    _library_map = {
        'Library name': 'name'
    }

    def handle(self, *args, **options):

        if options['verbose']:
            print >> sys.stderr, "delimiter is '{0}'".format(options['delimiter'])
            print >> sys.stderr, "quote character is '{0}'".format(options['quotechar'])

        data = []
        if len(args) and args[0][1] != '-':
            with open(args[0], 'r') as f:
                for row in csv.reader(f, delimiter=options['delimiter'], quotechar=options['quotechar']):
                    if len(data) == 0:
                        for label in row:
                            # 25 removes cruft after subject guide name
                            label = label.strip()[:25]

                            if label in self._guide_map:
                                data.append({
                                        'model': 'guide',
                                        'field': self._guide_map[label]
                                    })
                            elif label in self._librarian_map:
                                data.append({
                                        'model': 'librarian',
                                        'field': self._librarian_map[label]
                                    })
                            elif label in self._library_map:
                                data.append({
                                        'model': 'library',
                                        'field': self._library_map[label]
                                    })
                            else:
                                print >> sys.stderr, "Uknown column: '{0}'".format(label)
                                data.append({
                                        'model': 'unknown',
                                    })
                    else:
                        library = {}
                        librarian = {}
                        guide = {}
                        for i in range(len(data)):
                            val = row[i].strip()
                            if data[i]['model'] == 'library':
                                library[data[i]['field']] = val
                            elif data[i]['model'] == 'librarian':
                                librarian[data[i]['field']] = val
                            if data[i]['model'] == 'guide':
                                guide[data[i]['field']] = val

                        lib = None
                        if len(library[self._library_key]):
                            if options['verbose']:
                                print >> sys.stderr, 'library ref: {0}'.format(library[self._library_key])

                            try:
                                lib = Library.objects.get(**library)
                            except Library.DoesNotExist:
                                print >> sys.stderr, 'Missing library model: "{0}"'.format(library)
                                lib = None

                        libn = None
                        if len(librarian[self._librarian_key]):
                            if options['verbose']:
                                print >> sys.stderr, 'librarian ref: {0}'.format(librarian[self._librarian_key])

                            try:
                                libn = Librarian.objects.get(**librarian)
                            except Librarian.DoesNotExist:
                                libn = Librarian(**librarian)

                            libn.save()

                        if len(guide[self._guide_key]):
                            if options['verbose']:
                                print >> sys.stderr, 'subject guide ref: {0}'.format(guide[self._guide_key])

                            guide['library'] = lib
                            guide['librarian'] = libn
                            primary = { self._guide_key: guide[self._guide_key]}
                            try:
                                sg = SubjectGuide(**primary)
                                for (k, v) in guide.items():
                                    setattr(sg, k, v)

                            except SubjectGuide.DoesNotExist:
                                sg = SubjectGuide(**guide)

                            sg.save()
                            


