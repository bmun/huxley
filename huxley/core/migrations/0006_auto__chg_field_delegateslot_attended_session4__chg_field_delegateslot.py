# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'DelegateSlot.attended_session4'
        db.alter_column(u'delegate_slot', 'attended_session4', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'DelegateSlot.attended_session3'
        db.alter_column(u'delegate_slot', 'attended_session3', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'DelegateSlot.attended_session2'
        db.alter_column(u'delegate_slot', 'attended_session2', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'DelegateSlot.attended_session1'
        db.alter_column(u'delegate_slot', 'attended_session1', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

    def backwards(self, orm):

        # Changing field 'DelegateSlot.attended_session4'
        db.alter_column(u'delegate_slot', 'attended_session4', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'DelegateSlot.attended_session3'
        db.alter_column(u'delegate_slot', 'attended_session3', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'DelegateSlot.attended_session2'
        db.alter_column(u'delegate_slot', 'attended_session2', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'DelegateSlot.attended_session1'
        db.alter_column(u'delegate_slot', 'attended_session1', self.gf('django.db.models.fields.BooleanField')())

    models = {
        u'core.assignment': {
            'Meta': {'object_name': 'Assignment', 'db_table': "u'assignment'"},
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
            'Meta': {'object_name': 'Delegate', 'db_table': "u'delegate'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delegate_slot': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'related_name': "'delegate'", 'unique': 'True', 'null': 'True', 'to': u"orm['core.DelegateSlot']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'})
        },
        u'core.delegateslot': {
            'Meta': {'ordering': "['assignment__country']", 'object_name': 'DelegateSlot', 'db_table': "u'delegate_slot'"},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Assignment']"}),
            'attended_session1': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'attended_session2': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'attended_session3': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'attended_session4': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.helpcategory': {
            'Meta': {'object_name': 'HelpCategory', 'db_table': "u'help_category'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.helpquestion': {
            'Meta': {'object_name': 'HelpQuestion', 'db_table': "u'help_question'"},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.HelpCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.school': {
            'Meta': {'object_name': 'School', 'db_table': "u'school'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'committeepreferences': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Committee']", 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'countrypreferences': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Country']", 'through': u"orm['core.CountryPreference']", 'symmetrical': 'False'}),
            'delegation_fee': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'delegation_fee_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'delegation_fee_paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_delegation_size': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'min_delegation_size': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'primary_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'primary_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'primary_phone': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'program_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'registration_fee': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'registration_fee_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'registration_fee_paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'secondary_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'secondary_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'secondary_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'times_attended': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'waitlist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['core']