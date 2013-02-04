# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Participant.sum'
        db.add_column('main_app_participant', 'sum',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Participant.sum'
        db.delete_column('main_app_participant', 'sum')


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
            'sum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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