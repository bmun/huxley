# encoding: utf-8
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
        ))
        db.send_create_signal('cms', ['Country'])

        # Adding model 'Committee'
        db.create_table(u'Committee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='name', blank=True)),
        ))
        db.send_create_signal('cms', ['Committee'])

        # Adding model 'School'
        db.create_table(u'School', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateregistered', self.gf('django.db.models.fields.DateTimeField')(null=True, db_column='DateRegistered', blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolName', blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolAddress', blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolCity', blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolState', blank=True)),
            ('schoolzip', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolZip', blank=True)),
            ('primaryname', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='PrimaryName', blank=True)),
            ('primaryemail', self.gf('django.db.models.fields.EmailField')(max_length=765, db_column='PrimaryEmail', blank=True)),
            ('primaryphone', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='PrimaryPhone', blank=True)),
            ('secondaryname', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SecondaryName', blank=True)),
            ('secondaryemail', self.gf('django.db.models.fields.EmailField')(max_length=765, db_column='SecondaryEmail', blank=True)),
            ('secondaryphone', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SecondaryPhone', blank=True)),
            ('programtype', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='ProgramType', blank=True)),
            ('programattendance', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='ProgramAttendance')),
            ('mindelegation', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='MinimumDelegation')),
            ('maxdelegation', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='MaximumDelegation')),
            ('registrationpaid', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='RegistrationPaid', decimal_places=2, max_digits=4)),
            ('registrationowed', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='RegistrationOwed', decimal_places=2, max_digits=4)),
            ('registrationnet', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='RegistrationNet', decimal_places=2, max_digits=4)),
            ('delegationpaid', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='DelegationPaid', decimal_places=2, max_digits=4)),
            ('delegationowed', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='DelegationOwed', decimal_places=2, max_digits=4)),
            ('delegationnet', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='DelegationNet', decimal_places=2, max_digits=4)),
            ('international', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='International')),
        ))
        db.send_create_signal('cms', ['School'])

        # Adding model 'Assignment'
        db.create_table(u'Assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Committee'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Country'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['cms.School'], null=True, blank=True)),
        ))
        db.send_create_signal('cms', ['Assignment'])

        # Adding model 'DelegateSlot'
        db.create_table(u'DelegateSlot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Assignment'])),
        ))
        db.send_create_signal('cms', ['DelegateSlot'])

        # Adding model 'Delegate'
        db.create_table(u'Delegate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schoolid', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='SchoolID')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='Name', blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=765, db_column='Email', blank=True)),
            ('committee', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='Committee', blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='Country', blank=True)),
            ('delegateSlot', self.gf('django.db.models.fields.related.OneToOneField')(related_name='slot', unique=True, to=orm['cms.DelegateSlot'])),
        ))
        db.send_create_signal('cms', ['Delegate'])

        # Adding model 'Schools'
        db.create_table(u'Schools', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column='ID')),
            ('dateregistered', self.gf('django.db.models.fields.DateTimeField')(null=True, db_column='DateRegistered', blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='Username', blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='Password', blank=True)),
            ('schoolname', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolName', blank=True)),
            ('schooladdress', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolAddress', blank=True)),
            ('schoolcity', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolCity', blank=True)),
            ('schoolstate', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolState', blank=True)),
            ('schoolzip', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SchoolZip', blank=True)),
            ('primaryname', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='PrimaryName', blank=True)),
            ('primaryemail', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='PrimaryEmail', blank=True)),
            ('primaryphone', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='PrimaryPhone', blank=True)),
            ('secondaryname', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SecondaryName', blank=True)),
            ('secondaryemail', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SecondaryEmail', blank=True)),
            ('secondaryphone', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SecondaryPhone', blank=True)),
            ('programtype', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='ProgramType', blank=True)),
            ('programattendance', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='ProgramAttendance')),
            ('minimumdelegation', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='MinimumDelegation')),
            ('maximumdelegation', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='MaximumDelegation')),
            ('countrypref', self.gf('django.db.models.fields.TextField')(db_column='CountryPref', blank=True)),
            ('committeepref', self.gf('django.db.models.fields.TextField')(db_column='CommitteePref', blank=True)),
            ('blocka', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='BlockA', blank=True)),
            ('blockb', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='BlockB', blank=True)),
            ('unpbc', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='UNPBC', blank=True)),
            ('uncsw', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='UNCSW', blank=True)),
            ('icc', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='ICC', blank=True)),
            ('cs', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='CS', blank=True)),
            ('sc', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='SC', blank=True)),
            ('hsc', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='HSC', blank=True)),
            ('g20', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='G20', blank=True)),
            ('au', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='AU', blank=True)),
            ('oas', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='OAS', blank=True)),
            ('eu', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='EU', blank=True)),
            ('assigned', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='Assigned', blank=True)),
            ('registrationpaid', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='RegistrationPaid', decimal_places=2, max_digits=4)),
            ('registrationowed', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='RegistrationOwed', decimal_places=2, max_digits=4)),
            ('registrationnet', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='RegistrationNet', decimal_places=2, max_digits=4)),
            ('delegationpaid', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='DelegationPaid', decimal_places=2, max_digits=4)),
            ('delegationowed', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='DelegationOwed', decimal_places=2, max_digits=4)),
            ('delegationnet', self.gf('django.db.models.fields.DecimalField')(default=0, db_column='DelegationNet', decimal_places=2, max_digits=4)),
        ))
        db.send_create_signal('cms', ['Schools'])

        # Adding model 'Delegates'
        db.create_table(u'Delegates', (
            ('delegateid', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column='DelegateID')),
            ('schoolid', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='SchoolID')),
            ('delegatename', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='DelegateName', blank=True)),
            ('delegateemail', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='DelegateEmail', blank=True)),
            ('delegatecommittee', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='DelegateCommittee', blank=True)),
            ('delegatecountry', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='DelegateCountry', blank=True)),
        ))
        db.send_create_signal('cms', ['Delegates'])

        # Adding model 'HelpCategory'
        db.create_table(u'HelpCategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_column='Name')),
        ))
        db.send_create_signal('cms', ['HelpCategory'])

        # Adding model 'HelpQuestion'
        db.create_table(u'HelpQuestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.HelpCategory'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='Question')),
            ('answer', self.gf('django.db.models.fields.TextField')(db_column='Answer')),
        ))
        db.send_create_signal('cms', ['HelpQuestion'])

        # Adding model 'AuthGroup'
        db.create_table(u'auth_group', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=240)),
        ))
        db.send_create_signal('cms', ['AuthGroup'])

        # Adding model 'AuthGroupPermissions'
        db.create_table(u'auth_group_permissions', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('group_id', self.gf('django.db.models.fields.IntegerField')()),
            ('permission_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cms', ['AuthGroupPermissions'])

        # Adding model 'AuthMessage'
        db.create_table(u'auth_message', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('cms', ['AuthMessage'])

        # Adding model 'AuthPermission'
        db.create_table(u'auth_permission', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('content_type_id', self.gf('django.db.models.fields.IntegerField')()),
            ('codename', self.gf('django.db.models.fields.CharField')(unique=True, max_length=300)),
        ))
        db.send_create_signal('cms', ['AuthPermission'])

        # Adding model 'AuthUser'
        db.create_table(u'auth_user', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=90)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=225)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=384)),
            ('is_staff', self.gf('django.db.models.fields.IntegerField')()),
            ('is_active', self.gf('django.db.models.fields.IntegerField')()),
            ('is_superuser', self.gf('django.db.models.fields.IntegerField')()),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('cms', ['AuthUser'])

        # Adding model 'AuthUserGroups'
        db.create_table(u'auth_user_groups', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('group_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cms', ['AuthUserGroups'])

        # Adding model 'AuthUserUserPermissions'
        db.create_table(u'auth_user_user_permissions', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('permission_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cms', ['AuthUserUserPermissions'])

        # Adding model 'DjangoAdminLog'
        db.create_table(u'django_admin_log', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('action_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('content_type_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('object_repr', self.gf('django.db.models.fields.CharField')(max_length=600)),
            ('action_flag', self.gf('django.db.models.fields.IntegerField')()),
            ('change_message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('cms', ['DjangoAdminLog'])

        # Adding model 'DjangoContentType'
        db.create_table(u'django_content_type', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('app_label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=300)),
            ('model', self.gf('django.db.models.fields.CharField')(unique=True, max_length=300)),
        ))
        db.send_create_signal('cms', ['DjangoContentType'])

        # Adding model 'DjangoSession'
        db.create_table(u'django_session', (
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=120, primary_key=True)),
            ('session_data', self.gf('django.db.models.fields.TextField')()),
            ('expire_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('cms', ['DjangoSession'])

        # Adding model 'DjangoSite'
        db.create_table(u'django_site', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('cms', ['DjangoSite'])

        # Adding model 'UserProfile'
        db.create_table(u'UserProfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, blank=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(related_name='advisor', to=orm['cms.Schools'])),
            ('committee', self.gf('django.db.models.fields.CharField')(max_length=765, db_column='ChairCommittee', blank=True)),
        ))
        db.send_create_signal('cms', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table(u'Country')

        # Deleting model 'Committee'
        db.delete_table(u'Committee')

        # Deleting model 'School'
        db.delete_table(u'School')

        # Deleting model 'Assignment'
        db.delete_table(u'Assignment')

        # Deleting model 'DelegateSlot'
        db.delete_table(u'DelegateSlot')

        # Deleting model 'Delegate'
        db.delete_table(u'Delegate')

        # Deleting model 'Schools'
        db.delete_table(u'Schools')

        # Deleting model 'Delegates'
        db.delete_table(u'Delegates')

        # Deleting model 'HelpCategory'
        db.delete_table(u'HelpCategory')

        # Deleting model 'HelpQuestion'
        db.delete_table(u'HelpQuestion')

        # Deleting model 'AuthGroup'
        db.delete_table(u'auth_group')

        # Deleting model 'AuthGroupPermissions'
        db.delete_table(u'auth_group_permissions')

        # Deleting model 'AuthMessage'
        db.delete_table(u'auth_message')

        # Deleting model 'AuthPermission'
        db.delete_table(u'auth_permission')

        # Deleting model 'AuthUser'
        db.delete_table(u'auth_user')

        # Deleting model 'AuthUserGroups'
        db.delete_table(u'auth_user_groups')

        # Deleting model 'AuthUserUserPermissions'
        db.delete_table(u'auth_user_user_permissions')

        # Deleting model 'DjangoAdminLog'
        db.delete_table(u'django_admin_log')

        # Deleting model 'DjangoContentType'
        db.delete_table(u'django_content_type')

        # Deleting model 'DjangoSession'
        db.delete_table(u'django_session')

        # Deleting model 'DjangoSite'
        db.delete_table(u'django_site')

        # Deleting model 'UserProfile'
        db.delete_table(u'UserProfile')


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
        'cms.assignment': {
            'Meta': {'object_name': 'Assignment', 'db_table': "u'Assignment'"},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Committee']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['cms.School']", 'null': 'True', 'blank': 'True'})
        },
        'cms.authgroup': {
            'Meta': {'object_name': 'AuthGroup', 'db_table': "u'auth_group'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '240'})
        },
        'cms.authgrouppermissions': {
            'Meta': {'object_name': 'AuthGroupPermissions', 'db_table': "u'auth_group_permissions'"},
            'group_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'permission_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'cms.authmessage': {
            'Meta': {'object_name': 'AuthMessage', 'db_table': "u'auth_message'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'cms.authpermission': {
            'Meta': {'object_name': 'AuthPermission', 'db_table': "u'auth_permission'"},
            'codename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'content_type_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'cms.authuser': {
            'Meta': {'object_name': 'AuthUser', 'db_table': "u'auth_user'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '225'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.IntegerField', [], {}),
            'is_staff': ('django.db.models.fields.IntegerField', [], {}),
            'is_superuser': ('django.db.models.fields.IntegerField', [], {}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '384'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '90'})
        },
        'cms.authusergroups': {
            'Meta': {'object_name': 'AuthUserGroups', 'db_table': "u'auth_user_groups'"},
            'group_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'cms.authuseruserpermissions': {
            'Meta': {'object_name': 'AuthUserUserPermissions', 'db_table': "u'auth_user_user_permissions'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'permission_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'cms.committee': {
            'Meta': {'object_name': 'Committee', 'db_table': "u'Committee'"},
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cms.Country']", 'through': "orm['cms.Assignment']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'name'", 'blank': 'True'})
        },
        'cms.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'Country'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'name'", 'blank': 'True'})
        },
        'cms.delegate': {
            'Meta': {'object_name': 'Delegate', 'db_table': "u'Delegate'"},
            'committee': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'Committee'", 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'Country'", 'blank': 'True'}),
            'delegateSlot': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'slot'", 'unique': 'True', 'to': "orm['cms.DelegateSlot']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '765', 'db_column': "'Email'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'Name'", 'blank': 'True'}),
            'schoolid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'SchoolID'"})
        },
        'cms.delegates': {
            'Meta': {'object_name': 'Delegates', 'db_table': "u'Delegates'"},
            'delegatecommittee': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'DelegateCommittee'", 'blank': 'True'}),
            'delegatecountry': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'DelegateCountry'", 'blank': 'True'}),
            'delegateemail': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'DelegateEmail'", 'blank': 'True'}),
            'delegateid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'DelegateID'"}),
            'delegatename': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'DelegateName'", 'blank': 'True'}),
            'schoolid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'SchoolID'"})
        },
        'cms.delegateslot': {
            'Meta': {'object_name': 'DelegateSlot', 'db_table': "u'DelegateSlot'"},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Assignment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cms.djangoadminlog': {
            'Meta': {'object_name': 'DjangoAdminLog', 'db_table': "u'django_admin_log'"},
            'action_flag': ('django.db.models.fields.IntegerField', [], {}),
            'action_time': ('django.db.models.fields.DateTimeField', [], {}),
            'change_message': ('django.db.models.fields.TextField', [], {}),
            'content_type_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'object_repr': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'cms.djangocontenttype': {
            'Meta': {'object_name': 'DjangoContentType', 'db_table': "u'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'cms.djangosession': {
            'Meta': {'object_name': 'DjangoSession', 'db_table': "u'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '120', 'primary_key': 'True'})
        },
        'cms.djangosite': {
            'Meta': {'object_name': 'DjangoSite', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'cms.helpcategory': {
            'Meta': {'object_name': 'HelpCategory', 'db_table': "u'HelpCategory'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_column': "'Name'"})
        },
        'cms.helpquestion': {
            'Meta': {'object_name': 'HelpQuestion', 'db_table': "u'HelpQuestion'"},
            'answer': ('django.db.models.fields.TextField', [], {'db_column': "'Answer'"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.HelpCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'Question'"})
        },
        'cms.school': {
            'Meta': {'object_name': 'School', 'db_table': "u'School'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolAddress'", 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolCity'", 'blank': 'True'}),
            'dateregistered': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'DateRegistered'", 'blank': 'True'}),
            'delegationnet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationNet'", 'decimal_places': '2', 'max_digits': '4'}),
            'delegationowed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationOwed'", 'decimal_places': '2', 'max_digits': '4'}),
            'delegationpaid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationPaid'", 'decimal_places': '2', 'max_digits': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'International'"}),
            'maxdelegation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'MaximumDelegation'"}),
            'mindelegation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'MinimumDelegation'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolName'", 'blank': 'True'}),
            'primaryemail': ('django.db.models.fields.EmailField', [], {'max_length': '765', 'db_column': "'PrimaryEmail'", 'blank': 'True'}),
            'primaryname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'PrimaryName'", 'blank': 'True'}),
            'primaryphone': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'PrimaryPhone'", 'blank': 'True'}),
            'programattendance': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'ProgramAttendance'"}),
            'programtype': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'ProgramType'", 'blank': 'True'}),
            'registrationnet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationNet'", 'decimal_places': '2', 'max_digits': '4'}),
            'registrationowed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationOwed'", 'decimal_places': '2', 'max_digits': '4'}),
            'registrationpaid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationPaid'", 'decimal_places': '2', 'max_digits': '4'}),
            'schoolzip': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolZip'", 'blank': 'True'}),
            'secondaryemail': ('django.db.models.fields.EmailField', [], {'max_length': '765', 'db_column': "'SecondaryEmail'", 'blank': 'True'}),
            'secondaryname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SecondaryName'", 'blank': 'True'}),
            'secondaryphone': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SecondaryPhone'", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolState'", 'blank': 'True'})
        },
        'cms.schools': {
            'Meta': {'object_name': 'Schools', 'db_table': "u'Schools'"},
            'assigned': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'Assigned'", 'blank': 'True'}),
            'au': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'AU'", 'blank': 'True'}),
            'blocka': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'BlockA'", 'blank': 'True'}),
            'blockb': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'BlockB'", 'blank': 'True'}),
            'committeepref': ('django.db.models.fields.TextField', [], {'db_column': "'CommitteePref'", 'blank': 'True'}),
            'countrypref': ('django.db.models.fields.TextField', [], {'db_column': "'CountryPref'", 'blank': 'True'}),
            'cs': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'CS'", 'blank': 'True'}),
            'dateregistered': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'DateRegistered'", 'blank': 'True'}),
            'delegationnet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationNet'", 'decimal_places': '2', 'max_digits': '4'}),
            'delegationowed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationOwed'", 'decimal_places': '2', 'max_digits': '4'}),
            'delegationpaid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationPaid'", 'decimal_places': '2', 'max_digits': '4'}),
            'eu': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'EU'", 'blank': 'True'}),
            'g20': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'G20'", 'blank': 'True'}),
            'hsc': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'HSC'", 'blank': 'True'}),
            'icc': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'ICC'", 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'maximumdelegation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'MaximumDelegation'"}),
            'minimumdelegation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'MinimumDelegation'"}),
            'oas': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'OAS'", 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'Password'", 'blank': 'True'}),
            'primaryemail': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'PrimaryEmail'", 'blank': 'True'}),
            'primaryname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'PrimaryName'", 'blank': 'True'}),
            'primaryphone': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'PrimaryPhone'", 'blank': 'True'}),
            'programattendance': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'ProgramAttendance'"}),
            'programtype': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'ProgramType'", 'blank': 'True'}),
            'registrationnet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationNet'", 'decimal_places': '2', 'max_digits': '4'}),
            'registrationowed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationOwed'", 'decimal_places': '2', 'max_digits': '4'}),
            'registrationpaid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationPaid'", 'decimal_places': '2', 'max_digits': '4'}),
            'sc': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SC'", 'blank': 'True'}),
            'schooladdress': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolAddress'", 'blank': 'True'}),
            'schoolcity': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolCity'", 'blank': 'True'}),
            'schoolname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolName'", 'blank': 'True'}),
            'schoolstate': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolState'", 'blank': 'True'}),
            'schoolzip': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolZip'", 'blank': 'True'}),
            'secondaryemail': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SecondaryEmail'", 'blank': 'True'}),
            'secondaryname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SecondaryName'", 'blank': 'True'}),
            'secondaryphone': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SecondaryPhone'", 'blank': 'True'}),
            'uncsw': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'UNCSW'", 'blank': 'True'}),
            'unpbc': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'UNPBC'", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'Username'", 'blank': 'True'})
        },
        'cms.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "u'UserProfile'"},
            'committee': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'ChairCommittee'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'advisor'", 'to': "orm['cms.Schools']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cms']
