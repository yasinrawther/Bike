# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'BikeDetails.image'
        db.alter_column(u'bikedetails_bikedetails', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=200))

    def backwards(self, orm):

        # Changing field 'BikeDetails.image'
        db.alter_column(u'bikedetails_bikedetails', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

    models = {
        u'bikedetails.bikedetails': {
            'Meta': {'object_name': 'BikeDetails'},
            'bike_model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'bike_reg_no': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fuel_tank_capacity': ('django.db.models.fields.FloatField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'km_driven': ('django.db.models.fields.IntegerField', [], {'max_length': '20'}),
            'max_power': ('django.db.models.fields.IntegerField', [], {'max_length': '20'}),
            'milege': ('django.db.models.fields.FloatField', [], {'max_length': '20'}),
            'top_speed': ('django.db.models.fields.IntegerField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['bikedetails']