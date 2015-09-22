from django.core.management.base import BaseCommand
from optparse import make_option
from libguide.models import CurriculumGuide, SubjectGuide
from sis_provisioner.models import Curriculum
import sys
import csv


class Command(BaseCommand):
    help = "Load Library Models from csv - RUN ME LAST"

    option_list = BaseCommand.option_list + (
        make_option('--verbose', dest='verbose', default=False, help='Verbose mode'),
        make_option('--delimiter', dest='delimiter', default=',', help='CSV file delimiter'),
        make_option('--quotechar', dest='quotechar', default='"', help='CSV file quote character'),
    )

    _curriculum_field = 'curriculum_abbr'

    _subject_guide_field = 'name'

    # dictionary keys are CSV column headings, values are model field names
    _field_map = {
        'Curriculum code': 'curriculum_abbr',
        'Discipline name': 'discipline',
        'Subject guide name': 'name'
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
                            label = label.strip()

                            if label in self._field_map:
                                data.append({ 'field': self._field_map[label] })
                            else:
                                print >> sys.stderr, "Uknown column: '{0}'".format(label)
                                data.append({ 'field': label })

                    else:
                        columns = {}
                        for i in range(len(data)):
                            columns[data[i]['field']] = row[i].strip()

                        try:
                            if options['verbose']:
                                print >> sys.stderr, 'curriculum {0} = {1}'.format(self._curriculum_field,
                                                                                   columns[self._curriculum_field])

                                print >> sys.stderr, 'guide {0} = {1}'.format(self._subject_guide_field,
                                                                              columns[self._subject_guide_field])



                            if len(columns[self._curriculum_field]) and len(columns[self._subject_guide_field]):

                                primary = { self._curriculum_field: columns[self._curriculum_field] }

                                if options['verbose']:
                                    print >> sys.stderr, 'looking up Curriculum {0}'.format(primary)

                                curriculum = Curriculum.objects.get(**primary)

                                primary = { self._subject_guide_field: columns[self._subject_guide_field] }

                                if options['verbose']:
                                    print >> sys.stderr, 'looking up SubjectGuide {0}'.format(primary)

                                subject_guides = SubjectGuide.objects.filter(**primary)
                                if len(subject_guides):
                                    subject_guide = subject_guides.last()
                                else:
                                    print >> sys.stderr, 'Unknown Subject Guide reference "{0}"'.format(columns[self._subject_guide_field])
                                    continue

                                try:
                                    guide = CurriculumGuide.objects.get(curriculum=curriculum)
                                    guide.subject_guide = subject_guide

                                except CurriculumGuide.MultipleObjectsReturned:
                                    CurriculumGuide.objects.filter(curriculum=curriculum).delete()
                                    model = {
                                        'curriculum': curriculum,
                                        'subject_guide': subject_guide
                                    }
                                    guide = CurriculumGuide(**model)

                                except CurriculumGuide.DoesNotExist:
                                    model = {
                                        'curriculum': curriculum,
                                        'subject_guide': subject_guide
                                    }
                                    guide = CurriculumGuide(**model)

                                guide.save()

                        except SubjectGuide.DoesNotExist:
                            print >> sys.stderr, 'No SubjectGuide model: "{0}"'.format(columns[self._subject_guide_field])
                        except Curriculum.DoesNotExist:
                            print >> sys.stderr, 'No Curriculum model: "{0}"'.format(columns[self._curriculum_field])
                        except KeyError:
                            print >> sys.stderr, 'Missing Field'
