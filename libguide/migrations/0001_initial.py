# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sis_provisioner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurriculumGuide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('curriculum', models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.PROTECT, to='sis_provisioner.Curriculum')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Librarian',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, null=True)),
                ('email', models.CharField(max_length=512, null=True)),
                ('phone', models.CharField(max_length=512, null=True)),
                ('url', models.CharField(max_length=512, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, null=True)),
                ('description', models.CharField(max_length=8192, null=True)),
                ('url', models.CharField(max_length=512, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubjectGuide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, null=True)),
                ('label', models.CharField(max_length=1024, null=True)),
                ('url', models.CharField(max_length=512, null=True)),
                ('librarian', models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.PROTECT, to='libguide.Librarian', null=True)),
                ('library', models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.PROTECT, to='libguide.Library', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='curriculumguide',
            name='subject_guide',
            field=models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.PROTECT, to='libguide.SubjectGuide'),
            preserve_default=True,
        ),
    ]
