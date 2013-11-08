# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClassifiedCategory'
        db.create_table('main_classifieds_categories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('main', ['ClassifiedCategory'])

        # Adding model 'ClassifiedStatus'
        db.create_table('main_classifieds_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('main', ['ClassifiedStatus'])

        # Adding model 'Country'
        db.create_table('main_location_countries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=96)),
        ))
        db.send_create_signal('main', ['Country'])

        # Adding model 'Province'
        db.create_table('main_location_provinces', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Country'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=96)),
        ))
        db.send_create_signal('main', ['Province'])

        # Adding model 'City'
        db.create_table('main_location_cities', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('cp', self.gf('django.db.models.fields.IntegerField')(max_length=8)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Province'])),
            ('google_map', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal('main', ['City'])

        # Adding model 'Classified'
        db.create_table('main_classifieds', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ClassifiedCategory'])),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1, max_length=1)),
            ('type', self.gf('django.db.models.fields.CharField')(default='sale', max_length=12)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='peso_arg', max_length=12)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 8, 0, 0))),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.City'], null=True, blank=True)),
            ('contact_address', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('contact_email', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('google_map', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('visits', self.gf('django.db.models.fields.IntegerField')()),
            ('image_1', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('image_2', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('image_3', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('main', ['Classified'])

        # Adding model 'UserProfile'
        db.create_table('main_user_profile', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=64, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.City'], null=True, blank=True)),
        ))
        db.send_create_signal('main', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'ClassifiedCategory'
        db.delete_table('main_classifieds_categories')

        # Deleting model 'ClassifiedStatus'
        db.delete_table('main_classifieds_status')

        # Deleting model 'Country'
        db.delete_table('main_location_countries')

        # Deleting model 'Province'
        db.delete_table('main_location_provinces')

        # Deleting model 'City'
        db.delete_table('main_location_cities')

        # Deleting model 'Classified'
        db.delete_table('main_classifieds')

        # Deleting model 'UserProfile'
        db.delete_table('main_user_profile')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.city': {
            'Meta': {'object_name': 'City', 'db_table': "'main_location_cities'"},
            'cp': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'google_map': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Province']"})
        },
        'main.classified': {
            'Meta': {'object_name': 'Classified', 'db_table': "'main_classifieds'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ClassifiedCategory']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.City']", 'null': 'True', 'blank': 'True'}),
            'contact_address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'peso_arg'", 'max_length': '12'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 8, 0, 0)'}),
            'google_map': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image_2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image_3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'sale'", 'max_length': '12'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'visits': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.classifiedcategory': {
            'Meta': {'object_name': 'ClassifiedCategory', 'db_table': "'main_classifieds_categories'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'main.classifiedstatus': {
            'Meta': {'object_name': 'ClassifiedStatus', 'db_table': "'main_classifieds_status'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'main.country': {
            'Meta': {'object_name': 'Country', 'db_table': "'main_location_countries'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '96'})
        },
        'main.province': {
            'Meta': {'object_name': 'Province', 'db_table': "'main_location_provinces'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '96'})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "'main_user_profile'", '_ormbases': [u'auth.User']},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.City']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['main']