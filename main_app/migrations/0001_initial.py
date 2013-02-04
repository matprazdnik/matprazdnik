# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'School'
        db.create_table('main_app_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('city', self.gf('django.db.models.fields.CharField')(default='\xd0\x9c\xd0\xbe\xd1\x81\xd0\xba\xd0\xb2\xd0\xb0', max_length=64)),
            ('genitive', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('main_app', ['School'])

        # Adding model 'Participant'
        db.create_table('main_app_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('grade', self.gf('django.db.models.fields.IntegerField')(default=6)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_app.School'], null=True, blank=True)),
            ('points_1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('points_2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('points_3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('points_4', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('points_5', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('points_6a', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('points_6b', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('main_app', ['Participant'])


    def backwards(self, orm):
        # Deleting model 'School'
        db.delete_table('main_app_school')

        # Deleting model 'Participant'
        db.delete_table('main_app_participant')


    models = {
        'main_app.participant': {
            'Meta': {'object_name': 'Participant'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'grade': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'points_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'points_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'points_3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'points_4': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'points_5': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'points_6a': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'points_6b': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main_app.School']", 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'main_app.school': {
            'Meta': {'object_name': 'School'},
            'city': ('django.db.models.fields.CharField', [], {'default': "'\\xd0\\x9c\\xd0\\xbe\\xd1\\x81\\xd0\\xba\\xd0\\xb2\\xd0\\xb0'", 'max_length': '64'}),
            'genitive': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['main_app']