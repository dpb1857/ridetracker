# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('pbp2011_country')

        # Deleting field 'Rider.country'
        db.delete_column('pbp2011_rider', 'country_id')


    def backwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('pbp2011_country', (
            ('country_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2, unique=True)),
        ))
        db.send_create_signal('pbp2011', ['Country'])

        # User chose to not deal with backwards NULL issues for 'Rider.country'
        raise RuntimeError("Cannot reverse this migration. 'Rider.country' and its values cannot be restored.")


    models = {
        'pbp2011.biketype': {
            'Meta': {'object_name': 'BikeType'},
            'bike_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pbp2011.control': {
            'Meta': {'object_name': 'Control'},
            'cp1': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp10': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp11': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp12': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp13': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp14': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp15': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp2': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp3': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp4': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp5': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp6': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp7': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp8': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cp9': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'dnf': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dns': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'frame_number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'pbp2011.rider': {
            'Meta': {'object_name': 'Rider'},
            'bike_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pbp2011.BikeType']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'frame_number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'tmp_country_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'})
        }
    }

    complete_apps = ['pbp2011']
