# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('pbp2011_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('country_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
        ))
        db.send_create_signal('pbp2011', ['Country'])

        # Adding model 'BikeType'
        db.create_table('pbp2011_biketype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bike_type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
        ))
        db.send_create_signal('pbp2011', ['BikeType'])

        # Adding model 'Rider'
        db.create_table('pbp2011_rider', (
            ('frame_number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pbp2011.Country'])),
            ('bike_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pbp2011.BikeType'])),
        ))
        db.send_create_signal('pbp2011', ['Rider'])

        # Adding model 'Control'
        db.create_table('pbp2011_control', (
            ('frame_number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('dnf', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dns', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cp1', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp2', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp3', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp4', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp5', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp6', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp7', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp8', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp9', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp10', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp11', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp12', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp13', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp14', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp15', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('pbp2011', ['Control'])


    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('pbp2011_country')

        # Deleting model 'BikeType'
        db.delete_table('pbp2011_biketype')

        # Deleting model 'Rider'
        db.delete_table('pbp2011_rider')

        # Deleting model 'Control'
        db.delete_table('pbp2011_control')


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
        'pbp2011.country': {
            'Meta': {'object_name': 'Country'},
            'country_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pbp2011.rider': {
            'Meta': {'object_name': 'Rider'},
            'bike_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pbp2011.BikeType']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pbp2011.Country']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'frame_number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['pbp2011']
