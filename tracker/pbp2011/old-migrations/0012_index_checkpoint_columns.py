# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'Checkpoint', fields ['frame_number']
        db.create_index('pbp2011_checkpoint', ['frame_number'])

        # Adding index on 'Checkpoint', fields ['time']
        db.create_index('pbp2011_checkpoint', ['time'])


    def backwards(self, orm):
        
        # Removing index on 'Checkpoint', fields ['time']
        db.delete_index('pbp2011_checkpoint', ['time'])

        # Removing index on 'Checkpoint', fields ['frame_number']
        db.delete_index('pbp2011_checkpoint', ['frame_number'])


    models = {
        'pbp2011.biketype': {
            'Meta': {'object_name': 'BikeType'},
            'bike_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pbp2011.checkpoint': {
            'Meta': {'object_name': 'Checkpoint'},
            'checkpoint_number': ('django.db.models.fields.IntegerField', [], {}),
            'frame_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'pbp2011.rider': {
            'Meta': {'object_name': 'Rider'},
            'bike_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pbp2011.BikeType']"}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'dnf': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dns': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'frame_number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['pbp2011']
