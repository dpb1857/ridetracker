# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BikeType'
        db.create_table('pbp2011_biketype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bike_type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
        ))
        db.send_create_signal('pbp2011', ['BikeType'])

        # Adding model 'Control'
        db.create_table('pbp2011_control', (
            ('number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('distance', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('pbp2011', ['Control'])

        # Adding model 'Checkpoint'
        db.create_table('pbp2011_checkpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('checkpoint_number', self.gf('django.db.models.fields.IntegerField')()),
            ('frame_number', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal('pbp2011', ['Checkpoint'])

        # Adding model 'Rider'
        db.create_table('pbp2011_rider', (
            ('frame_number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('bike_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pbp2011.BikeType'])),
            ('dnf', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dns', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('pbp2011', ['Rider'])


    def backwards(self, orm):
        
        # Deleting model 'BikeType'
        db.delete_table('pbp2011_biketype')

        # Deleting model 'Control'
        db.delete_table('pbp2011_control')

        # Deleting model 'Checkpoint'
        db.delete_table('pbp2011_checkpoint')

        # Deleting model 'Rider'
        db.delete_table('pbp2011_rider')


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
        'pbp2011.control': {
            'Meta': {'object_name': 'Control'},
            'distance': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
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
