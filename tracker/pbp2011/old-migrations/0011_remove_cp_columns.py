# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Rider.cp12'
        db.delete_column('pbp2011_rider', 'cp12')

        # Deleting field 'Rider.cp13'
        db.delete_column('pbp2011_rider', 'cp13')

        # Deleting field 'Rider.cp10'
        db.delete_column('pbp2011_rider', 'cp10')

        # Deleting field 'Rider.cp11'
        db.delete_column('pbp2011_rider', 'cp11')

        # Deleting field 'Rider.cp14'
        db.delete_column('pbp2011_rider', 'cp14')

        # Deleting field 'Rider.cp15'
        db.delete_column('pbp2011_rider', 'cp15')

        # Deleting field 'Rider.cp8'
        db.delete_column('pbp2011_rider', 'cp8')

        # Deleting field 'Rider.cp9'
        db.delete_column('pbp2011_rider', 'cp9')

        # Deleting field 'Rider.cp1'
        db.delete_column('pbp2011_rider', 'cp1')

        # Deleting field 'Rider.cp2'
        db.delete_column('pbp2011_rider', 'cp2')

        # Deleting field 'Rider.cp3'
        db.delete_column('pbp2011_rider', 'cp3')

        # Deleting field 'Rider.cp4'
        db.delete_column('pbp2011_rider', 'cp4')

        # Deleting field 'Rider.cp5'
        db.delete_column('pbp2011_rider', 'cp5')

        # Deleting field 'Rider.cp6'
        db.delete_column('pbp2011_rider', 'cp6')

        # Deleting field 'Rider.cp7'
        db.delete_column('pbp2011_rider', 'cp7')


    def backwards(self, orm):
        
        # Adding field 'Rider.cp12'
        db.add_column('pbp2011_rider', 'cp12', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp13'
        db.add_column('pbp2011_rider', 'cp13', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp10'
        db.add_column('pbp2011_rider', 'cp10', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp11'
        db.add_column('pbp2011_rider', 'cp11', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp14'
        db.add_column('pbp2011_rider', 'cp14', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp15'
        db.add_column('pbp2011_rider', 'cp15', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp8'
        db.add_column('pbp2011_rider', 'cp8', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp9'
        db.add_column('pbp2011_rider', 'cp9', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp1'
        db.add_column('pbp2011_rider', 'cp1', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp2'
        db.add_column('pbp2011_rider', 'cp2', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp3'
        db.add_column('pbp2011_rider', 'cp3', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp4'
        db.add_column('pbp2011_rider', 'cp4', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp5'
        db.add_column('pbp2011_rider', 'cp5', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp6'
        db.add_column('pbp2011_rider', 'cp6', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp7'
        db.add_column('pbp2011_rider', 'cp7', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)


    models = {
        'pbp2011.biketype': {
            'Meta': {'object_name': 'BikeType'},
            'bike_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pbp2011.checkpoint': {
            'Meta': {'object_name': 'Checkpoint'},
            'checkpoint_number': ('django.db.models.fields.IntegerField', [], {}),
            'frame_number': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
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
