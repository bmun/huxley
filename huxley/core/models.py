# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.contrib.auth.models import User
from django.db import models

class Conference(models.Model):
    session         = models.PositiveSmallIntegerField(default=0)
    start_date      = models.DateField()
    end_date        = models.DateField()
    reg_open        = models.DateField()
    early_reg_close = models.DateField()
    reg_close       = models.DateField()
    min_attendance  = models.PositiveSmallIntegerField(default=0)
    max_attendance  = models.PositiveSmallIntegerField(default=0)
    
    def __unicode__(self):
        return 'BMUN %d' % self.session
    
    class Meta:
        db_table = u'conference'
        get_latest_by = 'start_date'


class Country(models.Model):
    name    = models.CharField(max_length=128)
    special = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'country'


class Committee(models.Model):
    name            = models.CharField(max_length=8)
    full_name       = models.CharField(max_length=128)
    countries       = models.ManyToManyField(Country, through='Assignment')
    delegation_size = models.PositiveSmallIntegerField(default=2)
    special         = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'committee'


class School(models.Model):
    TYPE_CLUB = 1
    TYPE_CLASS = 2
    PROGRAM_TYPE_OPTIONS = (
        (TYPE_CLUB, 'Club'),
        (TYPE_CLASS, 'Class'),
    )
    
    registered          = models.DateTimeField(auto_now_add=True)
    name                = models.CharField(max_length=128) 
    address             = models.CharField(max_length=128) 
    city                = models.CharField(max_length=128) 
    state               = models.CharField(max_length=16) 
    zip_code            = models.CharField(max_length=16) 
    primary_name        = models.CharField(max_length=128) 
    primary_email       = models.EmailField() 
    primary_phone       = models.CharField(max_length=32) 
    secondary_name      = models.CharField(max_length=128, blank=True) 
    secondary_email     = models.EmailField(blank=True) 
    secondary_phone     = models.CharField(max_length=32, blank=True) 
    program_type        = models.PositiveSmallIntegerField(choices=PROGRAM_TYPE_OPTIONS)
    times_attended      = models.PositiveSmallIntegerField(default=0)
    min_delegation_size = models.PositiveSmallIntegerField(default=0) 
    max_delegation_size = models.PositiveSmallIntegerField(default=0)
    international       = models.BooleanField(default=False)
    
    countrypreferences   = models.ManyToManyField(Country, through='CountryPreference')
    committeepreferences = models.ManyToManyField(Committee, limit_choices_to={'special':True})
    
    registration_fee         = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    registration_fee_paid    = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    registration_fee_balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    delegation_fee           = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    delegation_fee_paid      = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    delegation_fee_balance   = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def refresh_country_preferences(self, country_ids):
        """ Refreshes a school's country preferences, given a list of
            country IDs. """
        self.countrypreferences.clear()
        seen = set()
        for rank, country_id in enumerate(country_ids, start=1):
            if country_id and country_id not in seen:
                seen.add(country_id)
                CountryPreference.objects.create(school=self,
                                                 country_id=country_id,
                                                 rank=rank)
    
    def refresh_committee_preferences(self, committee_ids):
        """ Refreshes a school's committee preferences. """
        self.committeepreferences.clear()
        self.committeepreferences = committee_ids
        self.save()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'school'


class Assignment(models.Model):
    committee = models.ForeignKey(Committee)
    country   = models.ForeignKey(Country)
    school    = models.ForeignKey(School, null=True, blank=True, default=None)

    def __unicode__(self):
        return self.committee.name + " : " + self.country.name

    class Meta:
        db_table = u'assignment'


class CountryPreference(models.Model):
    school  = models.ForeignKey(School)
    country = models.ForeignKey(Country, limit_choices_to={'special':False})
    rank    = models.PositiveSmallIntegerField()
    
    @staticmethod
    def unshuffle(country_ids):
        """ Returns a list of country ids in correct, unshuffled order. """
        return country_ids[0::2] + country_ids[1::2]

    def __unicode__(self):
        return "%s : %s (%d)" % self.school.name, self.country.name, self.rank

    class Meta:
        db_table = u'country_preference'


class DelegateSlot(models.Model):
    assignment        = models.ForeignKey(Assignment)
    attended_session1 = models.BooleanField(default=False)
    attended_session2 = models.BooleanField(default=False)
    attended_session3 = models.BooleanField(default=False)
    attended_session4 = models.BooleanField(default=False)
    
    def update_or_create_delegate(self, delegate_data):
        """ Updates this slot's delegate object, or creates one if
            the slot has no delegate. """
        try:
            delegate = self.delegate
            for attr, value in delegate_data.items():
                setattr(delegate, attr, value)
            delegate.save()
        except Delegate.DoesNotExist:
            Delegate.objects.create(delegate_slot=self, **delegate_data)
    
    def delete_delegate_if_exists(self):
        """ Deletes this slot's delegate or fails silently. """
        try:
            self.delegate.delete()
        except Delegate.DoesNotExist:
            pass
    
    def update_delegate_attendance(self, slot_data):
        """ Updates this slot's attendance information. """
        self.attended_session1 = slot_data['session1']
        self.attended_session2 = slot_data['session2']
        self.attended_session3 = slot_data['session3']
        self.attended_session4 = slot_data['session4']
        self.save()

    @property
    def country(self):
        return self.assignment.country
    
    @property
    def committee(self):
        return self.assignment.committee
    
    @property
    def school(self):
        return self.assignment.school

    def __unicode__(self):
        return str(self.assignment)

    class Meta:
        db_table = u'delegate_slot'


class Delegate(models.Model):
    name          = models.CharField(max_length=64, blank=True) 
    email         = models.EmailField(blank=True) 
    delegate_slot = models.OneToOneField(DelegateSlot, related_name='delegate', null=True, default=None)
    created_at    = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
    @property
    def country(self):
        return self.delegate_slot.country
    
    @property
    def committee(self):
        return self.delegate_slot.committee
    
    @property
    def school(self):
        return self.delegate_slot.school

    class Meta:
        db_table = u'delegate'


class HelpCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'help_category'


class HelpQuestion(models.Model):
    category = models.ForeignKey(HelpCategory)
    question = models.CharField(max_length=255)
    answer   = models.TextField()
    
    def __unicode__(self):
        return self.question

    class Meta:
        db_table = u'help_question'


class AdvisorProfile(models.Model):
    user   = models.OneToOneField(User, related_name='advisor_profile')
    school = models.ForeignKey(School, related_name='advisor_profile')
    
    def __unicode__(self):
        return self.user.username

    class Meta:
        db_table = u'advisor_profile'


class SecretariatProfile(models.Model):
    user      = models.OneToOneField(User, related_name='secretariat_profile')
    committee = models.ForeignKey(Committee, related_name='secretariat_profile')

    def __unicode__(self):
        return self.user.username
    
    class Meta:
        db_table = u'secretariat_profile'
