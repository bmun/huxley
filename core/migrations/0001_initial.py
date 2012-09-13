# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'Country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='name', blank=True)),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='special')),
        ))
        db.send_create_signal('core', ['Country'])

        # Adding model 'Committee'
        db.create_table(u'Committee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='name', blank=True)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='fullname', blank=True)),
            ('delegatesperdelegation', self.gf('django.db.models.fields.IntegerField')(default=2, db_column='delegatesperdelegation')),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='special')),
        ))
        db.send_create_signal('core', ['Committee'])

        # Adding model 'School'
        db.create_table(u'School', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateregistered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_column='DateRegistered', blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolName', blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolAddress', blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolCity', blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolState', blank=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolZip', blank=True)),
            ('primaryname', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='PrimaryName', blank=True)),
            ('primaryemail', self.gf('django.db.models.fields.EmailField')(max_length=765, db_column='PrimaryEmail', blank=True)),
            ('primaryphone', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='PrimaryPhone', blank=True)),
            ('secondaryname', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SecondaryName', blank=True)),
            ('secondaryemail', self.gf('django.db.models.fields.EmailField')(max_length=765, db_column='SecondaryEmail', blank=True)),
            ('secondaryphone', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SecondaryPhone', blank=True)),
            ('programtype', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='ProgramType', blank=True)),
            ('timesattended', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='TimesAttended')),
            ('mindelegationsize', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='MinimumDelegationSize')),
            ('maxdelegationsize', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='MaximumDelegationSize')),
            ('registrationpaid', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='RegistrationPaid', decimal_places=2, max_digits=6)),
            ('registrationowed', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='RegistrationOwed', decimal_places=2, max_digits=6)),
            ('registrationnet', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='RegistrationNet', decimal_places=2, max_digits=6)),
            ('delegationpaid', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='DelegationPaid', decimal_places=2, max_digits=6)),
            ('delegationowed', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='DelegationOwed', decimal_places=2, max_digits=6)),
            ('delegationnet', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='DelegationNet', decimal_places=2, max_digits=6)),
            ('international', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='International')),
        ))
        db.send_create_signal('core', ['School'])

        # Adding M2M table for field committeepreferences on 'School'
        db.create_table(u'School_committeepreferences', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('school', models.ForeignKey(orm['core.school'], null=False)),
            ('committee', models.ForeignKey(orm['core.committee'], null=False))
        ))
        db.create_unique(u'School_committeepreferences', ['school_id', 'committee_id'])

        # Adding model 'Assignment'
        db.create_table(u'Assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Committee'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Country'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['core.School'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Assignment'])

        # Adding model 'CountryPreference'
        db.create_table(u'CountryPreference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.School'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Country'])),
            ('rank', self.gf('django.db.models.fields.IntegerField')(default=1, db_column='rank')),
        ))
        db.send_create_signal('core', ['CountryPreference'])

        # Adding model 'DelegateSlot'
        db.create_table(u'DelegateSlot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Assignment'])),
        ))
        db.send_create_signal('core', ['DelegateSlot'])

        # Adding model 'Delegate'
        db.create_table(u'Delegate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='Name', blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=765, db_column='Email', blank=True)),
            ('delegateslot', self.gf('django.db.models.fields.related.OneToOneField')(default=None, related_name='delegate', unique=True, null=True, to=orm['core.DelegateSlot'])),
        ))
        db.send_create_signal('core', ['Delegate'])

        # Adding model 'HelpCategory'
        db.create_table(u'HelpCategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_column='Name')),
        ))
        db.send_create_signal('core', ['HelpCategory'])

        # Adding model 'HelpQuestion'
        db.create_table(u'HelpQuestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.HelpCategory'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='Question')),
            ('answer', self.gf('django.db.models.fields.TextField')(db_column='Answer')),
        ))
        db.send_create_signal('core', ['HelpQuestion'])

        # Adding model 'AdvisorProfile'
        db.create_table(u'AdvisorProfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='advisor_profile', unique=True, blank=True, to=orm['auth.User'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(related_name='advisor_profile', to=orm['core.School'])),
        ))
        db.send_create_signal('core', ['AdvisorProfile'])

        # Adding model 'SecretariatProfile'
        db.create_table(u'SecretariatProfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='secretariat_profile', unique=True, blank=True, to=orm['auth.User'])),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='secretariat_profile', to=orm['core.Committee'])),
            ('is_sg', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_tech', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_internal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_external', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_outreach', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_publication', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_research', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['SecretariatProfile'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'Country')

        # Deleting model 'Committee'
        db.delete_table(u'Committee')

        # Deleting model 'School'
        db.delete_table(u'School')

        # Removing M2M table for field committeepreferences on 'School'
        db.delete_table('School_committeepreferences')

        # Deleting model 'Assignment'
        db.delete_table(u'Assignment')

        # Deleting model 'CountryPreference'
        db.delete_table(u'CountryPreference')

        # Deleting model 'DelegateSlot'
        db.delete_table(u'DelegateSlot')

        # Deleting model 'Delegate'
        db.delete_table(u'Delegate')

        # Deleting model 'HelpCategory'
        db.delete_table(u'HelpCategory')

        # Deleting model 'HelpQuestion'
        db.delete_table(u'HelpQuestion')

        # Deleting model 'AdvisorProfile'
        db.delete_table(u'AdvisorProfile')

        # Deleting model 'SecretariatProfile'
        db.delete_table(u'SecretariatProfile')


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
            'delegateslot': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'related_name': "'delegate'", 'unique': 'True', 'null': 'True', 'to': "orm['core.DelegateSlot']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '765', 'db_column': "'Email'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'Name'", 'blank': 'True'})
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