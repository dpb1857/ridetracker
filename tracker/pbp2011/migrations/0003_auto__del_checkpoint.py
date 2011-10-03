# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Checkpoint'
        db.delete_table('pbp2011_checkpoint')


    def backwards(self, orm):
        
        # Adding model 'Checkpoint'
        db.create_table('pbp2011_checkpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('frame_number', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('checkpoint_number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('pbp2011', ['Checkpoint'])

        control_map = {}
        for control in orm.Control.objects.order_by('number'):
            control_map[int(control.distance)] = control

        for waypoint in orm.Waypoint.objects.all():
            checkpoint = orm.Checkpoint()
            checkpoint.time = waypoint.timestamp
            checkpoint.checkpoint_number = control_map[int(waypoint.kilometers)].number
            checkpoint.frame_number = waypoint.frame_key_id
            checkpoint.save()

    models = {
        'pbp2011.biketype': {
            'Meta': {'object_name': 'BikeType'},
            'bike_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        },
        'pbp2011.waypoint': {
            'Meta': {'object_name': 'Waypoint'},
            'data_source': ('django.db.models.fields.IntegerField', [], {}),
            'frame_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pbp2011.Rider']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kilometers': ('django.db.models.fields.FloatField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'transition': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['pbp2011']
