# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from pbp2011.models import Waypoint

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Waypoint'
        db.create_table('pbp2011_waypoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('frame_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pbp2011.Rider'])),
            ('kilometers', self.gf('django.db.models.fields.FloatField')()),
            ('transition', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('data_source', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('pbp2011', ['Waypoint'])

        controls = list(orm.Control.objects.order_by('number'))

        rider_map = {}
        for rider in orm.Rider.objects.all():
            rider_map[rider.frame_number] = rider

        for checkpoint in orm.Checkpoint.objects.all():
            waypoint = orm.Waypoint()
            waypoint.kilometers = controls[checkpoint.checkpoint_number-1].distance
            waypoint.timestamp = checkpoint.time
            waypoint.transition = Waypoint.TRANSITION_ARRIVAL
            waypoint.data_source = Waypoint.SOURCE_SYSTEM
            waypoint.frame_key = rider_map[checkpoint.frame_number]
            waypoint.save()

    def backwards(self, orm):
        
        # Deleting model 'Waypoint'
        db.delete_table('pbp2011_waypoint')


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
