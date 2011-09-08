# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Control'
        db.delete_table('pbp2011_control')


    def backwards(self, orm):
        
        # Adding model 'Control'
        db.create_table('pbp2011_control', (
            ('frame_number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('cp3', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp7', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('dnf', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cp5', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp8', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp9', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp6', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('dns', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cp13', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp12', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp1', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp10', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp11', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp4', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp2', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp14', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cp15', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('pbp2011', ['Control'])


    models = {
        'pbp2011.biketype': {
            'Meta': {'object_name': 'BikeType'},
            'bike_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pbp2011.rider': {
            'Meta': {'object_name': 'Rider'},
            'bike_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pbp2011.BikeType']"}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
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
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'frame_number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['pbp2011']
