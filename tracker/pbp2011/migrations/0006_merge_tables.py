# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Rider.tmp_country_code'
        db.delete_column('pbp2011_rider', 'tmp_country_code')

        # Adding field 'Rider.dnf'
        db.add_column('pbp2011_rider', 'dnf', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Rider.dns'
        db.add_column('pbp2011_rider', 'dns', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

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

        # Adding field 'Rider.cp8'
        db.add_column('pbp2011_rider', 'cp8', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp9'
        db.add_column('pbp2011_rider', 'cp9', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp10'
        db.add_column('pbp2011_rider', 'cp10', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp11'
        db.add_column('pbp2011_rider', 'cp11', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp12'
        db.add_column('pbp2011_rider', 'cp12', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp13'
        db.add_column('pbp2011_rider', 'cp13', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp14'
        db.add_column('pbp2011_rider', 'cp14', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Rider.cp15'
        db.add_column('pbp2011_rider', 'cp15', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        for rider in orm.Rider.objects.all():
            control = orm.Control.objects.get(frame_number=rider.frame_number)
            for i in range(1, 16):
                attr = "cp%d" % i
                setattr(rider, attr, getattr(control, attr))
                
            rider.dns = control.dns
            rider.dnf = control.dnf

            rider.save()


    def backwards(self, orm):
        
        # Adding field 'Rider.tmp_country_code'
        db.add_column('pbp2011_rider', 'tmp_country_code', self.gf('django.db.models.fields.CharField')(max_length=2, null=True), keep_default=False)

        # Deleting field 'Rider.dnf'
        db.delete_column('pbp2011_rider', 'dnf')

        # Deleting field 'Rider.dns'
        db.delete_column('pbp2011_rider', 'dns')

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

        # Deleting field 'Rider.cp8'
        db.delete_column('pbp2011_rider', 'cp8')

        # Deleting field 'Rider.cp9'
        db.delete_column('pbp2011_rider', 'cp9')

        # Deleting field 'Rider.cp10'
        db.delete_column('pbp2011_rider', 'cp10')

        # Deleting field 'Rider.cp11'
        db.delete_column('pbp2011_rider', 'cp11')

        # Deleting field 'Rider.cp12'
        db.delete_column('pbp2011_rider', 'cp12')

        # Deleting field 'Rider.cp13'
        db.delete_column('pbp2011_rider', 'cp13')

        # Deleting field 'Rider.cp14'
        db.delete_column('pbp2011_rider', 'cp14')

        # Deleting field 'Rider.cp15'
        db.delete_column('pbp2011_rider', 'cp15')


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
