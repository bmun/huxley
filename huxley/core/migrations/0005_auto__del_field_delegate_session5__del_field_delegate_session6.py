# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Delegate.session5'
        db.delete_column(u'Delegate', 'session5')

        # Deleting field 'Delegate.session6'
        db.delete_column(u'Delegate', 'session6')


    def backwards(self, orm):
        # Adding field 'Delegate.session5'
        db.add_column(u'Delegate', 'session5',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Delegate.session6'
        db.add_column(u'Delegate', 'session6',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.advisorprofile': {
            'Meta': {'object_name': 'AdvisorProfile', 'db_table': "u'AdvisorProfile'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'advisor_profile'", 'to': "orm['core.School']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'advisor_profile'", 'unique': 'True', 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'core.assignment': {
            'Meta': {'object_name': 'Assignment', 'db_table': "u'Assignment'"},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Committee']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['core.School']", 'null': 'True', 'blank': 'True'})
        },
        'core.committee': {
            'Meta': {'object_name': 'Committee', 'db_table': "u'Committee'"},
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Country']", 'through': "orm['core.Assignment']", 'symmetrical': 'False'}),
            'delegatesperdelegation': ('django.db.models.fields.IntegerField', [], {'default': '2', 'db_column': "'delegatesperdelegation'"}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'fullname'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'name'", 'blank': 'True'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'special'"})
        },
        'core.conference': {
            'Meta': {'object_name': 'Conference', 'db_table': "u'Conference'"},
            'earlyregistrationend': ('django.db.models.fields.DateField', [], {'db_column': "'EarlyRegistrationEnd'"}),
            'enddate': ('django.db.models.fields.DateField', [], {'db_column': "'EndDate'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxattendance': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'MaxAttendance'"}),
            'minattendance': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'MinAttendance'"}),
            'registrationend': ('django.db.models.fields.DateField', [], {'db_column': "'RegistrationEnd'"}),
            'registrationstart': ('django.db.models.fields.DateField', [], {'db_column': "'RegistrationStart'"}),
            'session': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'Session'"}),
            'startdate': ('django.db.models.fields.DateField', [], {'db_column': "'StartDate'"})
        },
        'core.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'Country'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'name'", 'blank': 'True'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'special'"})
        },
        'core.countrypreference': {
            'Meta': {'object_name': 'CountryPreference', 'db_table': "u'CountryPreference'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_column': "'rank'"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.School']"})
        },
        'core.delegate': {
            'Meta': {'object_name': 'Delegate', 'db_table': "u'Delegate'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'delegateslot': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'related_name': "'delegate'", 'unique': 'True', 'null': 'True', 'to': "orm['core.DelegateSlot']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '765', 'db_column': "'Email'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'Name'", 'blank': 'True'}),
            'session1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session4': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.delegateslot': {
            'Meta': {'object_name': 'DelegateSlot', 'db_table': "u'DelegateSlot'"},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Assignment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.helpcategory': {
            'Meta': {'object_name': 'HelpCategory', 'db_table': "u'HelpCategory'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_column': "'Name'"})
        },
        'core.helpquestion': {
            'Meta': {'object_name': 'HelpQuestion', 'db_table': "u'HelpQuestion'"},
            'answer': ('django.db.models.fields.TextField', [], {'db_column': "'Answer'"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.HelpCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'Question'"})
        },
        'core.school': {
            'Meta': {'object_name': 'School', 'db_table': "u'School'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolAddress'", 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolCity'", 'blank': 'True'}),
            'committeepreferences': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['core.Committee']", 'symmetrical': 'False', 'db_column': "'CommitteePreferences'", 'blank': 'True'}),
            'countrypreferences': ('django.db.models.fields.related.ManyToManyField', [], {'db_column': "'CountryPreferences'", 'default': 'None', 'to': "orm['core.Country']", 'through': "orm['core.CountryPreference']", 'blank': 'True', 'symmetrical': 'False'}),
            'dateregistered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_column': "'DateRegistered'", 'blank': 'True'}),
            'delegationnet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationNet'", 'decimal_places': '2', 'max_digits': '6'}),
            'delegationowed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationOwed'", 'decimal_places': '2', 'max_digits': '6'}),
            'delegationpaid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationPaid'", 'decimal_places': '2', 'max_digits': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'International'"}),
            'maxdelegationsize': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'MaximumDelegationSize'"}),
            'mindelegationsize': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'MinimumDelegationSize'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolName'", 'blank': 'True'}),
            'primaryemail': ('django.db.models.fields.EmailField', [], {'max_length': '765', 'db_column': "'PrimaryEmail'", 'blank': 'True'}),
            'primaryname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'PrimaryName'", 'blank': 'True'}),
            'primaryphone': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'PrimaryPhone'", 'blank': 'True'}),
            'programtype': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'ProgramType'", 'blank': 'True'}),
            'registrationnet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationNet'", 'decimal_places': '2', 'max_digits': '6'}),
            'registrationowed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationOwed'", 'decimal_places': '2', 'max_digits': '6'}),
            'registrationpaid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationPaid'", 'decimal_places': '2', 'max_digits': '6'}),
            'secondaryemail': ('django.db.models.fields.EmailField', [], {'max_length': '765', 'db_column': "'SecondaryEmail'", 'blank': 'True'}),
            'secondaryname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SecondaryName'", 'blank': 'True'}),
            'secondaryphone': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SecondaryPhone'", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolState'", 'blank': 'True'}),
            'timesattended': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'TimesAttended'"}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolZip'", 'blank': 'True'})
        },
        'core.secretariatprofile': {
            'Meta': {'object_name': 'SecretariatProfile', 'db_table': "u'SecretariatProfile'"},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secretariat_profile'", 'to': "orm['core.Committee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_internal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_outreach': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_publication': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_research': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sg': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_tech': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'secretariat_profile'", 'unique': 'True', 'blank': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['core']