# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Library'
        db.create_table('libguide_library', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=8192, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
        ))
        db.send_create_signal('libguide', ['Library'])

        # Adding model 'Librarian'
        db.create_table('libguide_librarian', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
        ))
        db.send_create_signal('libguide', ['Librarian'])

        # Adding model 'SubjectGuide'
        db.create_table('libguide_subjectguide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('library', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, on_delete=models.PROTECT, to=orm['libguide.Library'])),
            ('librarian', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, on_delete=models.PROTECT, to=orm['libguide.Librarian'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
        ))
        db.send_create_signal('libguide', ['SubjectGuide'])

        # Adding model 'CurriculumGuide'
        db.create_table('libguide_curriculumguide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('curriculum', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', on_delete=models.PROTECT, to=orm['sis_provisioner.Curriculum'])),
            ('subject_guide', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', on_delete=models.PROTECT, to=orm['libguide.SubjectGuide'])),
        ))
        db.send_create_signal('libguide', ['CurriculumGuide'])


    def backwards(self, orm):
        # Deleting model 'Library'
        db.delete_table('libguide_library')

        # Deleting model 'Librarian'
        db.delete_table('libguide_librarian')

        # Deleting model 'SubjectGuide'
        db.delete_table('libguide_subjectguide')

        # Deleting model 'CurriculumGuide'
        db.delete_table('libguide_curriculumguide')


    models = {
        'libguide.curriculumguide': {
            'Meta': {'object_name': 'CurriculumGuide'},
            'curriculum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'on_delete': 'models.PROTECT', 'to': "orm['sis_provisioner.Curriculum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject_guide': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'on_delete': 'models.PROTECT', 'to': "orm['libguide.SubjectGuide']"})
        },
        'libguide.librarian': {
            'Meta': {'object_name': 'Librarian'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'})
        },
        'libguide.library': {
            'Meta': {'object_name': 'Library'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'})
        },
        'libguide.subjectguide': {
            'Meta': {'object_name': 'SubjectGuide'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'librarian': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['libguide.Librarian']"}),
            'library': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['libguide.Library']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'})
        },
        'sis_provisioner.curriculum': {
            'Meta': {'object_name': 'Curriculum'},
            'curriculum_abbr': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '20'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subaccount_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['libguide']