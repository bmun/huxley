# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from datetime import datetime
from decimal import Decimal

class Conference(models.Model):
    session =  models.IntegerField(db_column='Session', default=0)
    startdate = models.DateField(db_column='StartDate')
    enddate = models.DateField(db_column='EndDate')
    registrationstart = models.DateField(db_column='RegistrationStart')
    earlyregistrationend = models.DateField(db_column='EarlyRegistrationEnd')
    registrationend = models.DateField(db_column='RegistrationEnd')
    minattendance = models.IntegerField(db_column='MinAttendance', default=0)
    maxattendance = models.IntegerField(db_column='MaxAttendance', default=0)
    class Meta:
        db_table = u'Conference'
        get_latest_by = 'startdate'
    def __unicode__(self):
        return 'BMUN ' + str(self.session)


class Country(models.Model):
    name = models.CharField(max_length=765, db_column='name', null=False, blank=True)
    special = models.BooleanField(null=False, blank=False, db_column="special", default=False)
    class Meta:
        db_table = u'Country'
    def __unicode__(self):
        return self.name


class Committee(models.Model):
    name = models.CharField(max_length=765, db_column='name', null=False, blank=True)
    fullname = models.CharField(max_length=765, db_column='fullname', null=False, blank=True)
    countries = models.ManyToManyField(Country, through='Assignment')
    delegatesperdelegation = models.IntegerField(db_column='delegatesperdelegation', default=2, blank=False, null=False)
    special = models.BooleanField(null=False, blank=False, db_column="special", default=False)
    class Meta:
        db_table = u'Committee'
    def __unicode__(self):
        return self.name


class School(models.Model):
    
    PROGRAM_TYPE_OPTIONS = (
	('club', 'Club'),
	('class', 'Class'),
    )
    
    dateregistered = models.DateTimeField(null=False, blank=False, db_column='DateRegistered', auto_now_add=True)
    name = models.CharField(max_length=765, db_column='SchoolName', blank=True) 
    address = models.CharField(max_length=765, db_column='SchoolAddress', blank=True) 
    city = models.CharField(max_length=765, db_column='SchoolCity', blank=True) 
    state = models.CharField(max_length=765, db_column='SchoolState', blank=True) 
    zip = models.CharField(max_length=765, db_column='SchoolZip', blank=True) 
    primaryname = models.CharField(max_length=765, db_column='PrimaryName', blank=True) 
    primaryemail = models.EmailField(max_length=765, db_column='PrimaryEmail', blank=True) 
    primaryphone = models.CharField(max_length=765, db_column='PrimaryPhone', blank=True) 
    secondaryname = models.CharField(max_length=765, db_column='SecondaryName', blank=True) 
    secondaryemail = models.EmailField(max_length=765, db_column='SecondaryEmail', blank=True) 
    secondaryphone = models.CharField(max_length=765, db_column='SecondaryPhone', blank=True) 
    programtype = models.CharField(max_length=765, db_column='ProgramType', blank=True, choices=PROGRAM_TYPE_OPTIONS) 
    timesattended = models.IntegerField(db_column='TimesAttended', default=0)
    mindelegationsize = models.IntegerField(db_column='MinimumDelegationSize', default=0) 
    maxdelegationsize = models.IntegerField(db_column='MaximumDelegationSize', default=0)
    countrypreferences = models.ManyToManyField(Country, db_column='CountryPreferences', blank=True, default=None, through='CountryPreference')
    committeepreferences = models.ManyToManyField(Committee, db_column='CommitteePreferences', limit_choices_to={'special':True}, blank=True, default=None)
    registrationpaid = models.DecimalField(max_digits=6, decimal_places=2, db_column='RegistrationPaid', default=0) 
    registrationowed = models.DecimalField(max_digits=6, decimal_places=2, db_column='RegistrationOwed', default=0) 
    registrationnet = models.DecimalField(max_digits=6, decimal_places=2, db_column='RegistrationNet', default=0) 
    delegationpaid = models.DecimalField(max_digits=6, decimal_places=2, db_column='DelegationPaid', default=0) 
    delegationowed = models.DecimalField(max_digits=6, decimal_places=2, db_column='DelegationOwed', default=0) 
    delegationnet = models.DecimalField(max_digits=6, decimal_places=2, db_column='DelegationNet', default=0) 
    international = models.BooleanField(null=False, db_column='International', default=False)
    class Meta:
        db_table = u'School'
    def __unicode__(self):
        return self.name


class Assignment(models.Model):
    committee = models.ForeignKey(Committee)
    country = models.ForeignKey(Country)
    school = models.ForeignKey(School, null=True, blank=True, default=None)
    class Meta:
        db_table = u'Assignment'
    def __unicode__(self):
        return self.committee.name + " : " + self.country.name


class CountryPreference(models.Model):
    school = models.ForeignKey(School)
    country = models.ForeignKey(Country, limit_choices_to={'special':False})
    rank = models.IntegerField(db_column='rank', null=False, blank=False, default=1)
    class Meta:
        db_table = u'CountryPreference'
    def __unicode__(self):
        return self.school.name + " : " + self.country.name + " (" + str(self.rank) + ")"


class DelegateSlot(models.Model):
    assignment = models.ForeignKey(Assignment)
    class Meta:
        db_table = u'DelegateSlot'
    def __unicode__(self):
        return self.assignment.__str__()
    def get_country(self):
        return self.assignment.country
    def get_committee(self):
        return self.assignment.committee
    def get_school(self):
        return self.assignment.school


class Delegate(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    email = models.EmailField(max_length=765, db_column='Email', blank=True) 
    delegateslot = models.OneToOneField(DelegateSlot, related_name='delegate', null=True, default=None, unique=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    session1 = models.BooleanField(default=False)
    session2 = models.BooleanField(default=False)
    session3 = models.BooleanField(default=False)
    session4 = models.BooleanField(default=False)
    session5 = models.BooleanField(default=False)
    session6 = models.BooleanField(default=False)
    class Meta:
        db_table = u'Delegate'
    def __unicode__(self):
        return self.name
    def get_country(self):
        return self.delegateslot.get_country()
    def get_committee(self):
        return self.delegateslot.get_committee()
    def get_school(self):
        return self.delegateslot.get_school()
    def attended_session(self, num):
        session = "session%d" % (num)
        field = getattr(self, session)
        return field


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


class AdvisorProfile(models.Model):
    user = models.OneToOneField(User, blank=True, related_name='advisor_profile')
    school = models.ForeignKey(School, related_name='advisor_profile')
    class Meta:
        db_table = u'AdvisorProfile'
    def __unicode__(self):
        return self.user.username


class SecretariatProfile(models.Model):
    user = models.OneToOneField(User, blank=True, related_name='secretariat_profile')
    committee = models.ForeignKey(Committee, related_name='secretariat_profile')
    is_sg = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_tech = models.BooleanField(default=False)
    is_internal = models.BooleanField(default=False)
    is_external = models.BooleanField(default=False)
    is_outreach = models.BooleanField(default=False)
    is_publication = models.BooleanField(default=False)
    is_research = models.BooleanField(default=False)
    class Meta:
        db_table = u'SecretariatProfile'


# --------------------
# Signals and Handlers
# --------------------

def create_delegate_slots(sender, **kwargs):
    if kwargs["created"]:
    	asmt = kwargs["instance"]
    	num_slots = asmt.committee.delegatesperdelegation
    	for slot in range(0, num_slots):
    	    DelegateSlot(assignment=asmt).save()

"""	
def delete_delegate_slots(sender, **kwargs):
    asmt = kwargs["instance"]
    for slot in DelegateSlot.objects.filter(assignment=asmt):
	   slot.delete()
"""

post_save.connect(create_delegate_slots, sender=Assignment)
#pre_delete.connect(delete_delegate_slots, sender=Assignment)

def net_registration_fee(sender, **kwargs):
   school = kwargs["instance"]
   school.registrationnet = school.registrationowed - school.registrationpaid
   print school.registrationnet

pre_save.connect(net_registration_fee, sender=School)

# Add and subtract delegate fees from a school when delegates are added
# and deleted.
"""
def add_delegate_fee(sender, **kwargs):
    if kwargs["created"]:
        early_deadline = datetime(2013, 2, 12)
        regular_deadline = datetime(2013, 2, 26)
        delegate = kwargs["instance"]
        school = delegate.get_school()
        
        if delegate.created_at < early_deadline:
            school.delegationowed += Decimal.from_float(40.00)
        elif delegate.created_at < regular_deadline:
            school.delegationowed += Decimal.from_float(50.00)
        else:
            school.delegationowed += Decimal.from_float(55.00)
        school.save()

def subtract_delegate_fee(sender, **kwargs):
    early_deadline = datetime(2013, 2, 12)
    regular_deadline = datetime(2013, 2, 26)
    delegate = kwargs["instance"]
    school = delegate.get_school()

    if delegate.created_at < early_deadline:
        school.delegationowed -= Decimal.from_float(40.00)
    elif delegate.created_at < regular_deadline:
        school.delegationowed -= Decimal.from_float(50.00)
    else:
        school.delegationowed -= Decimal.from_float(55.00)
    school.save()

post_save.connect(add_delegate_fee, sender=Delegate)
post_delete.connect(subtract_delegate_fee, sender=Delegate)
"""
