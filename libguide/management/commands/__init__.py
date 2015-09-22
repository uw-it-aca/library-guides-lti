"""
Libguide Import Routines

Typically, authoritative spreadsheet data is downloaded in csv form to
the data directory in /data/canvas/var.  Then the data is loaded into models
via:

  ./manage.py import_libraries /data/canvas/var/data/Draft-Libraries-Canvas-Mapping-Libraries.csv
                                                                                                                              
  ./manage.py import_subject_guides /data/canvas/var/data/Draft-Libraries-Canvas-Mapping-Subject-Guides.csv

  ./manage.py import_curriculum_guides /data/canvas/var/data/Draft-Libraries-Canvas-Mapping-CurriculumToSubject.csv

The order is important.  They'll add new rows, and update existing Library,
SubjectGuide and Librarian models with common "name" fields.
                                                                                                                              
They write to stderr any inconsistencies they find.  For example, there are a couple dozen or so unrecognized curriculum      
abbreviations.  Also, some of the librarian phone numbers and urls are backwards.                                             
                                                                                                                              
"""
