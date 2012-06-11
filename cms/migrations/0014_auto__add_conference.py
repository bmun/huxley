# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Conference'
        db.create_table(u'Conference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.IntegerField')(default=60, db_column='session')),
            ('registrationstart', self.gf('django.db.models.fields.DateField')(db_column='registrationstart')),
            ('earlyregistrationend', self.gf('django.db.models.fields.DateField')(db_column='earlyregistrationend')),
            ('registrationend', self.gf('django.db.models.fields.DateField')(db_column='registrationend')),
            ('assignmentsposted', self.gf('django.db.models.fields.DateField')(db_column='assignmentsposted')),
            ('conferencestart', self.gf('django.db.models.fields.DateField')(db_column='conferencestart')),
            ('conferenceend', self.gf('django.db.models.fields.DateField')(db_column='conferenceend')),
            ('sg', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unused1', db_column='sg', to=orm['auth.User'])),
            ('techofficer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unused2', db_column='techofficer', to=orm['auth.User'])),
            ('externalofficer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unused3', db_column='externalofficer', to=orm['auth.User'])),
            ('researchofficer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unused4', db_column='researchofficer', to=orm['auth.User'])),
            ('publicationsofficer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unused5', db_column='publicationsofficer', to=orm['auth.User'])),
        ))
        db.send_create_signal('cms', ['Conference'])


    def backwards(self, orm):
        
        # Deleting model 'Conference'
        db.delete_table(u'Conference')


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
            'delegatesperdelegation': ('django.db.models.fields.IntegerField', [], {'default': '2', 'db_column': "'delegatesperdelegation'"}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'fullname'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'name'", 'blank': 'True'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'special'"})
        },
        'cms.conference': {
            'Meta': {'object_name': 'Conference', 'db_table': "u'Conference'"},
            'assignmentsposted': ('django.db.models.fields.DateField', [], {'db_column': "'assignmentsposted'"}),
            'conferenceend': ('django.db.models.fields.DateField', [], {'db_column': "'conferenceend'"}),
            'conferencestart': ('django.db.models.fields.DateField', [], {'db_column': "'conferencestart'"}),
            'earlyregistrationend': ('django.db.models.fields.DateField', [], {'db_column': "'earlyregistrationend'"}),
            'externalofficer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unused3'", 'db_column': "'externalofficer'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publicationsofficer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unused5'", 'db_column': "'publicationsofficer'", 'to': "orm['auth.User']"}),
            'registrationend': ('django.db.models.fields.DateField', [], {'db_column': "'registrationend'"}),
            'registrationstart': ('django.db.models.fields.DateField', [], {'db_column': "'registrationstart'"}),
            'researchofficer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unused4'", 'db_column': "'researchofficer'", 'to': "orm['auth.User']"}),
            'session': ('django.db.models.fields.IntegerField', [], {'default': '60', 'db_column': "'session'"}),
            'sg': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unused1'", 'db_column': "'sg'", 'to': "orm['auth.User']"}),
            'techofficer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unused2'", 'db_column': "'techofficer'", 'to': "orm['auth.User']"})
        },
        'cms.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'Country'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'name'", 'blank': 'True'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'special'"})
        },
        'cms.countrypreference': {
            'Meta': {'object_name': 'CountryPreference', 'db_table': "u'CountryPreference'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_column': "'rank'"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.School']"})
        },
        'cms.delegate': {
            'Meta': {'object_name': 'Delegate', 'db_table': "u'Delegate'"},
            'delegateslot': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'related_name': "'delegate'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.DelegateSlot']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '765', 'db_column': "'Email'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'Name'", 'blank': 'True'})
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
            'committeepreferences': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['cms.Committee']", 'symmetrical': 'False', 'db_column': "'CommitteePreferences'", 'blank': 'True'}),
            'countrypreferences': ('django.db.models.fields.related.ManyToManyField', [], {'db_column': "'CountryPreferences'", 'default': 'None', 'to': "orm['cms.Country']", 'through': "orm['cms.CountryPreference']", 'blank': 'True', 'symmetrical': 'False'}),
            'dateregistered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_column': "'DateRegistered'", 'blank': 'True'}),
            'delegationnet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationNet'", 'decimal_places': '2', 'max_digits': '4'}),
            'delegationowed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationOwed'", 'decimal_places': '2', 'max_digits': '4'}),
            'delegationpaid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'DelegationPaid'", 'decimal_places': '2', 'max_digits': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'International'"}),
            'maxdelegationsize': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'MaximumDelegationSize'"}),
            'mindelegationsize': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'MinimumDelegationSize'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolName'", 'blank': 'True'}),
            'primaryemail': ('django.db.models.fields.EmailField', [], {'max_length': '765', 'db_column': "'PrimaryEmail'", 'blank': 'True'}),
            'primaryname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'PrimaryName'", 'blank': 'True'}),
            'primaryphone': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'PrimaryPhone'", 'blank': 'True'}),
            'programtype': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'ProgramType'", 'blank': 'True'}),
            'registrationnet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationNet'", 'decimal_places': '2', 'max_digits': '4'}),
            'registrationowed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationOwed'", 'decimal_places': '2', 'max_digits': '4'}),
            'registrationpaid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'db_column': "'RegistrationPaid'", 'decimal_places': '2', 'max_digits': '4'}),
            'secondaryemail': ('django.db.models.fields.EmailField', [], {'max_length': '765', 'db_column': "'SecondaryEmail'", 'blank': 'True'}),
            'secondaryname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SecondaryName'", 'blank': 'True'}),
            'secondaryphone': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SecondaryPhone'", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolState'", 'blank': 'True'}),
            'timesattended': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'TimesAttended'"}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'SchoolZip'", 'blank': 'True'})
        },
        'cms.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "u'UserProfile'"},
            'committee': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'ChairCommittee'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'advisor'", 'to': "orm['cms.School']"}),
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
