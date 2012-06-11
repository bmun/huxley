# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.contrib.auth.models import User

class Countrymatrix(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    blocka = models.IntegerField(db_column='BlockA') 
    blockb = models.IntegerField(db_column='BlockB') 
    unpbc = models.IntegerField(db_column='UNPBC') 
    uncsw = models.IntegerField(db_column='UNCSW') 
    au = models.IntegerField(db_column='AU') 
    eu = models.IntegerField(db_column='EU') 
    g20 = models.IntegerField(db_column='G20') 
    hsc = models.IntegerField(db_column='HSC') 
    oas = models.IntegerField(db_column='OAS') 
    icc = models.IntegerField(db_column='ICC') 
    sc = models.IntegerField(db_column='SC') 
    cs = models.IntegerField(db_column='CS') 
    class Meta:
        db_table = u'CountryMatrix'

class Schools(models.Model):
    
    PROGRAM_TYPE_OPTIONS = (
	('club', 'Club'),
	('class', 'Class'),
    )
    
    id = models.IntegerField(primary_key=True, db_column='ID') 
    dateregistered = models.DateTimeField(null=True, db_column='DateRegistered', blank=True) 
    username = models.CharField(max_length=765, db_column='Username', blank=True) 
    password = models.CharField(max_length=765, db_column='Password', blank=True) 
    schoolname = models.CharField(max_length=765, db_column='SchoolName', blank=True) 
    schooladdress = models.CharField(max_length=765, db_column='SchoolAddress', blank=True) 
    schoolcity = models.CharField(max_length=765, db_column='SchoolCity', blank=True) 
    schoolstate = models.CharField(max_length=765, db_column='SchoolState', blank=True) 
    schoolzip = models.CharField(max_length=765, db_column='SchoolZip', blank=True) 
    primaryname = models.CharField(max_length=765, db_column='PrimaryName', blank=True) 
    primaryemail = models.CharField(max_length=765, db_column='PrimaryEmail', blank=True) 
    primaryphone = models.CharField(max_length=765, db_column='PrimaryPhone', blank=True) 
    secondaryname = models.CharField(max_length=765, db_column='SecondaryName', blank=True) 
    secondaryemail = models.CharField(max_length=765, db_column='SecondaryEmail', blank=True) 
    secondaryphone = models.CharField(max_length=765, db_column='SecondaryPhone', blank=True) 
    programtype = models.CharField(max_length=765, db_column='ProgramType', blank=True, choices=PROGRAM_TYPE_OPTIONS) 
    programattendance = models.IntegerField(db_column='ProgramAttendance', default=0)
    minimumdelegation = models.IntegerField(db_column='MinimumDelegation', default=0) 
    maximumdelegation = models.IntegerField(db_column='MaximumDelegation', default=0) 
    countrypref = models.TextField(db_column='CountryPref', blank=True) 
    committeepref = models.TextField(db_column='CommitteePref', blank=True) 
    blocka = models.CharField(max_length=765, db_column='BlockA', blank=True) 
    blockb = models.CharField(max_length=765, db_column='BlockB', blank=True) 
    unpbc = models.CharField(max_length=765, db_column='UNPBC', blank=True) 
    uncsw = models.CharField(max_length=765, db_column='UNCSW', blank=True) 
    icc = models.CharField(max_length=765, db_column='ICC', blank=True) 
    cs = models.CharField(max_length=765, db_column='CS', blank=True) 
    sc = models.CharField(max_length=765, db_column='SC', blank=True) 
    hsc = models.CharField(max_length=765, db_column='HSC', blank=True) 
    g20 = models.CharField(max_length=765, db_column='G20', blank=True) 
    au = models.CharField(max_length=765, db_column='AU', blank=True) 
    oas = models.CharField(max_length=765, db_column='OAS', blank=True) 
    eu = models.CharField(max_length=765, db_column='EU', blank=True) 
    assigned = models.CharField(max_length=765, db_column='Assigned', blank=True) 
    registrationpaid = models.DecimalField(max_digits=4, decimal_places=2, db_column='RegistrationPaid', default=0) 
    registrationowed = models.DecimalField(max_digits=4, decimal_places=2, db_column='RegistrationOwed', default=0) 
    registrationnet = models.DecimalField(max_digits=4, decimal_places=2, db_column='RegistrationNet', default=0) 
    delegationpaid = models.DecimalField(max_digits=4, decimal_places=2, db_column='DelegationPaid', default=0) 
    delegationowed = models.DecimalField(max_digits=4, decimal_places=2, db_column='DelegationOwed', default=0) 
    delegationnet = models.DecimalField(max_digits=4, decimal_places=2, db_column='DelegationNet', default=0) 
    #international = models.BooleanField(null=False, db_column='International', blank=True, default=False)
    class Meta:
        db_table = u'Schools'
    def __unicode__(self):
	return self.schoolname

class Delegates(models.Model):
    delegateid = models.IntegerField(primary_key=True, db_column='DelegateID')
    #delegateschool = models.ForeignKey(Schools)
    schoolid = models.IntegerField(null=True, db_column='SchoolID') 
    delegatename = models.CharField(max_length=765, db_column='DelegateName', blank=True) 
    delegateemail = models.CharField(max_length=765, db_column='DelegateEmail', blank=True) 
    delegatecommittee = models.CharField(max_length=765, db_column='DelegateCommittee', blank=True) 
    delegatecountry = models.CharField(max_length=765, db_column='DelegateCountry', blank=True) 
    class Meta:
        db_table = u'Delegates'
    def __unicode__(self):
	return self.delegatename

class Scores(models.Model):
    delegateid = models.IntegerField(primary_key=True, db_column='DelegateID') 
    delegatecommittee = models.CharField(max_length=765, db_column='DelegateCommittee') 
    delegatecountry = models.CharField(max_length=765, db_column='DelegateCountry') 
    speeches = models.FloatField(null=True, db_column='Speeches', blank=True) 
    numspeeches = models.IntegerField(null=True, db_column='NumSpeeches', blank=True) 
    comments = models.FloatField(null=True, db_column='Comments', blank=True) 
    numcomments = models.IntegerField(null=True, db_column='NumComments', blank=True) 
    questions = models.FloatField(null=True, db_column='Questions', blank=True) 
    numquestions = models.IntegerField(null=True, db_column='NumQuestions', blank=True) 
    unmoderated = models.FloatField(null=True, db_column='Unmoderated', blank=True) 
    numunmoderated = models.IntegerField(null=True, db_column='NumUnmoderated', blank=True) 
    moderated = models.FloatField(null=True, db_column='Moderated', blank=True) 
    nummoderated = models.IntegerField(null=True, db_column='NumModerated', blank=True) 
    formal = models.FloatField(null=True, db_column='Formal', blank=True) 
    numformal = models.IntegerField(null=True, db_column='NumFormal', blank=True) 
    resolutions = models.FloatField(null=True, db_column='Resolutions', blank=True) 
    numresolutions = models.IntegerField(null=True, db_column='NumResolutions', blank=True) 
    amendments = models.FloatField(null=True, db_column='Amendments', blank=True) 
    numamendments = models.IntegerField(null=True, db_column='NumAmendments', blank=True) 
    diplomacy = models.FloatField(null=True, db_column='Diplomacy', blank=True) 
    numdiplomacy = models.IntegerField(null=True, db_column='NumDiplomacy', blank=True) 
    positionpaper = models.FloatField(null=True, db_column='PositionPaper', blank=True) 
    total = models.FloatField(null=True, db_column='Total', blank=True) 
    chaircomments = models.TextField(db_column='ChairComments', blank=True) 
    class Meta:
        db_table = u'Scores'

class HelpCategory(models.Model):
    name = models.CharField(unique=True, max_length=255, db_column="Name")
    class Meta:
	db_table = u'HelpCategory'
    def __unicode__(self):
	return self.name

class HelpQuestion(models.Model):
    category = models.ForeignKey(HelpCategory)
    question = models.CharField(max_length=255, db_column='Question')
    answer = models.TextField(db_column='Answer')
    class Meta:
	db_table = u'HelpQuestion'
    def __unicode__(self):
	return self.question

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=240)
    class Meta:
        db_table = u'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField()
    permission_id = models.IntegerField()
    class Meta:
        db_table = u'auth_group_permissions'

class AuthMessage(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    message = models.TextField()
    class Meta:
        db_table = u'auth_message'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    content_type_id = models.IntegerField()
    codename = models.CharField(unique=True, max_length=300)
    class Meta:
        db_table = u'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=90)
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=384)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = u'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    group_id = models.IntegerField()
    class Meta:
        db_table = u'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    permission_id = models.IntegerField()
    class Meta:
        db_table = u'auth_user_user_permissions'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user_id = models.IntegerField()
    content_type_id = models.IntegerField(null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=600)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = u'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    app_label = models.CharField(unique=True, max_length=300)
    model = models.CharField(unique=True, max_length=300)
    class Meta:
        db_table = u'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=120, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = u'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=300)
    name = models.CharField(max_length=150)
    class Meta:
        db_table = u'django_site'

class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=True)
    school = models.ForeignKey(Schools, related_name='advisor')
    committee = models.CharField(max_length=765, db_column='ChairCommittee', blank=True)
    class Meta:
        permissions = (
            ("can_edit_profile", "Can edit their personal profile."),
            ("can_mod_roster", "Can modify their roster."),
            ("can_check_attnd", "Can check the delegates' attendance."),
            ("can_take_attnd", "Can take committee attendance."),
            ("can_grade", "Can grade delegates in committee."),
            ("can_req_documents", "Can issue missing document requests to OPI")
        )
        db_table = u'UserProfile'
                                                               
