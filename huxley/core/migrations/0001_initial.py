# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Conference'
        db.create_table(u'conference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('reg_open', self.gf('django.db.models.fields.DateField')()),
            ('early_reg_close', self.gf('django.db.models.fields.DateField')()),
            ('reg_close', self.gf('django.db.models.fields.DateField')()),
            ('min_attendance', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('max_attendance', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['Conference'])

        # Adding model 'Country'
        db.create_table(u'country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['Country'])

        # Adding model 'Committee'
        db.create_table(u'committee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('delegation_size', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['Committee'])

        # Adding model 'School'
        db.create_table(u'school', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('registered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('primary_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('primary_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('primary_phone', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('secondary_name', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('secondary_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('secondary_phone', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('program_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('times_attended', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('min_delegation_size', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('max_delegation_size', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('international', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('registration_fee', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=2)),
            ('registration_fee_paid', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=2)),
            ('registration_fee_balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=2)),
            ('delegation_fee', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=2)),
            ('delegation_fee_paid', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=2)),
            ('delegation_fee_balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal(u'core', ['School'])

        # Adding M2M table for field committeepreferences on 'School'
        m2m_table_name = db.shorten_name(u'school_committeepreferences')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('school', models.ForeignKey(orm[u'core.school'], null=False)),
            ('committee', models.ForeignKey(orm[u'core.committee'], null=False))
        ))
        db.create_unique(m2m_table_name, ['school_id', 'committee_id'])

        # Adding model 'Assignment'
        db.create_table(u'assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Committee'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Country'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['core.School'], null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Assignment'])

        # Adding model 'CountryPreference'
        db.create_table(u'country_preference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.School'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Country'])),
            ('rank', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'core', ['CountryPreference'])

        # Adding model 'DelegateSlot'
        db.create_table(u'delegate_slot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Assignment'])),
            ('attended_session1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attended_session2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attended_session3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attended_session4', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['DelegateSlot'])

        # Adding model 'Delegate'
        db.create_table(u'delegate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('delegate_slot', self.gf('django.db.models.fields.related.OneToOneField')(default=None, related_name='delegate', unique=True, null=True, to=orm['core.DelegateSlot'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Delegate'])

        # Adding model 'HelpCategory'
        db.create_table(u'help_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'core', ['HelpCategory'])

        # Adding model 'HelpQuestion'
        db.create_table(u'help_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.HelpCategory'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['HelpQuestion'])


    def backwards(self, orm):
        # Deleting model 'Conference'
        db.delete_table(u'conference')

        # Deleting model 'Country'
        db.delete_table(u'country')

        # Deleting model 'Committee'
        db.delete_table(u'committee')

        # Deleting model 'School'
        db.delete_table(u'school')

        # Removing M2M table for field committeepreferences on 'School'
        db.delete_table(db.shorten_name(u'school_committeepreferences'))

        # Deleting model 'Assignment'
        db.delete_table(u'assignment')

        # Deleting model 'CountryPreference'
        db.delete_table(u'country_preference')

        # Deleting model 'DelegateSlot'
        db.delete_table(u'delegate_slot')

        # Deleting model 'Delegate'
        db.delete_table(u'delegate')

        # Deleting model 'HelpCategory'
        db.delete_table(u'help_category')

        # Deleting model 'HelpQuestion'
        db.delete_table(u'help_question')


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
            'reg_close': ('django.db.models.fields.DateField', [], {}),
            'reg_open': ('django.db.models.fields.DateField', [], {}),
            'session': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'core.delegateslot': {
            'Meta': {'object_name': 'DelegateSlot', 'db_table': "u'delegate_slot'"},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Assignment']"}),
            'attended_session1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attended_session2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attended_session3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attended_session4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['core']