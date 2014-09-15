# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DelegateSlot'
        db.delete_table(u'delegate_slot')

        # Deleting field 'Delegate.delegate_slot'
        db.delete_column(u'delegate', 'delegate_slot_id')

        # Adding field 'Delegate.assignment'
        db.add_column(u'delegate', 'assignment',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='delegates', to=orm['core.Assignment']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'DelegateSlot'
        db.create_table(u'delegate_slot', (
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Assignment'])),
            ('attended_session4', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('attended_session3', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('attended_session2', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('attended_session1', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'core', ['DelegateSlot'])

        # Adding field 'Delegate.delegate_slot'
        db.add_column(u'delegate', 'delegate_slot',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=None, related_name='delegate', unique=True, null=True, to=orm['core.DelegateSlot']),
                      keep_default=False)

        # Deleting field 'Delegate.assignment'
        db.delete_column(u'delegate', 'assignment_id')


    models = {
        u'core.assignment': {
            'Meta': {'unique_together': "(('committee', 'country'),)", 'object_name': 'Assignment', 'db_table': "u'assignment'"},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Committee']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['core.School']", 'null': 'True', 'blank': 'True'})
        },
        u'core.committee': {
            'Meta': {'object_name': 'Committee', 'db_table': "u'committee'"},
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Country']", 'through': u"orm['core.Assignment']", 'symmetrical': 'False'}),
            'delegation_size': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'core.conference': {
            'Meta': {'object_name': 'Conference', 'db_table': "u'conference'"},
            'early_reg_close': ('django.db.models.fields.DateField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_attendance': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'min_attendance': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'open_reg': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reg_close': ('django.db.models.fields.DateField', [], {}),
            'reg_open': ('django.db.models.fields.DateField', [], {}),
            'session': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'waitlist_reg': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'core.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'country'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'core.countrypreference': {
            'Meta': {'ordering': "['rank']", 'object_name': 'CountryPreference', 'db_table': "u'country_preference'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.School']"})
        },
        u'core.delegate': {
            'Meta': {'ordering': "['assignment__country']", 'object_name': 'Delegate', 'db_table': "u'delegate'"},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'delegates'", 'to': u"orm['core.Assignment']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'})
        },
        u'core.school': {
            'Meta': {'object_name': 'School', 'db_table': "u'school'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'advanced_delegates': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'beginner_delegates': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'countrypreferences': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Country']", 'through': u"orm['core.CountryPreference']", 'symmetrical': 'False'}),
            'fees_owed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'fees_paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intermediate_delegates': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'prefers_alternative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prefers_bilingual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prefers_crisis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prefers_press_corps': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prefers_specialized_regional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'primary_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'primary_gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'}),
            'primary_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'primary_phone': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'primary_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'program_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'registration_comments': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'secondary_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'secondary_gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4', 'blank': 'True'}),
            'secondary_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'secondary_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'secondary_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2', 'blank': 'True'}),
            'spanish_speaking_delegates': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'times_attended': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'waitlist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['core']