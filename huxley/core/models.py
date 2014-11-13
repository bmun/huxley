# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf import settings
from django.core.mail import send_mail
from django.db import models, transaction
from django.db.models.signals import post_save, pre_save

from huxley.core.constants import ContactGender, ContactType, ProgramTypes


class Conference(models.Model):
    session         = models.PositiveSmallIntegerField(default=0)
    start_date      = models.DateField()
    end_date        = models.DateField()
    reg_open        = models.DateField()
    early_reg_close = models.DateField()
    reg_close       = models.DateField()
    min_attendance  = models.PositiveSmallIntegerField(default=0)
    max_attendance  = models.PositiveSmallIntegerField(default=0)
    open_reg        = models.BooleanField(default=True)
    waitlist_reg    = models.BooleanField(default=False)

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
    REGISTRATION_FEE = 50.0
    DELEGATE_FEE = 50.0

    PROGRAM_TYPE_OPTIONS = (
        (ProgramTypes.CLUB, 'Club'),
        (ProgramTypes.CLASS, 'Class'),
    )

    CONTACT_TYPE_OPTIONS = (
        (ContactType.FACULTY, 'Faculty'),
        (ContactType.STUDENT, 'Student'),
    )

    GENDER_OPTIONS = (
        (ContactGender.MALE, 'Male'),
        (ContactGender.FEMALE, 'Female'),
        (ContactGender.OTHER, 'Other'),
        (ContactGender.UNSPECIFIED, 'Unspecified'),
    )

    registered          = models.DateTimeField(auto_now_add=True)
    name                = models.CharField(max_length=128)
    address             = models.CharField(max_length=128)
    city                = models.CharField(max_length=128)
    state               = models.CharField(max_length=16)
    zip_code            = models.CharField(max_length=16)
    country             = models.CharField(max_length=64)
    primary_name        = models.CharField(max_length=128)
    primary_gender      = models.PositiveSmallIntegerField(choices=GENDER_OPTIONS, default=ContactGender.UNSPECIFIED)
    primary_email       = models.EmailField()
    primary_phone       = models.CharField(max_length=32)
    primary_type        = models.PositiveSmallIntegerField(choices=CONTACT_TYPE_OPTIONS, default=ContactType.FACULTY)
    secondary_name      = models.CharField(max_length=128, blank=True)
    secondary_gender    = models.PositiveSmallIntegerField(choices=GENDER_OPTIONS, blank=True, default=ContactGender.UNSPECIFIED)
    secondary_email     = models.EmailField(blank=True)
    secondary_phone     = models.CharField(max_length=32, blank=True)
    secondary_type      = models.PositiveSmallIntegerField(choices=CONTACT_TYPE_OPTIONS, blank=True, default=ContactType.FACULTY)
    program_type        = models.PositiveSmallIntegerField(choices=PROGRAM_TYPE_OPTIONS, default=ProgramTypes.CLUB)
    times_attended      = models.PositiveSmallIntegerField(default=0)
    international       = models.BooleanField(default=False)
    waitlist            = models.BooleanField(default=False)

    beginner_delegates         = models.PositiveSmallIntegerField()
    intermediate_delegates     = models.PositiveSmallIntegerField()
    advanced_delegates         = models.PositiveSmallIntegerField()
    spanish_speaking_delegates = models.PositiveSmallIntegerField()

    countrypreferences   = models.ManyToManyField(Country, through='CountryPreference')

    prefers_bilingual            = models.BooleanField(default=False)
    prefers_specialized_regional = models.BooleanField(default=False)
    prefers_crisis               = models.BooleanField(default=False)
    prefers_alternative          = models.BooleanField(default=False)
    prefers_press_corps          = models.BooleanField(default=False)

    registration_comments = models.TextField(default='', blank=True)

    fees_owed = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fees_paid = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def update_country_preferences(self, country_ids):
        '''Given a list of country IDs, first dedupe and filter out 0s, then
        clear the existing country preferences and construct new ones.'''
        seen = set()
        processed_country_ids = []
        country_preferences = []

        for rank, country_id in enumerate(country_ids):
            if not country_id or country_id in seen:
                continue
            seen.add(country_id)
            processed_country_ids.append(country_id)
            country_preferences.append(
                CountryPreference(
                    school=self,
                    country_id=country_id,
                    rank=rank,
                )
            )

        if country_preferences:
            with transaction.atomic():
                self.countrypreferences.clear()
                CountryPreference.objects.bulk_create(country_preferences)

        return processed_country_ids

    @classmethod
    def update_fees(cls, **kwargs):
        school = kwargs['instance']
        delegate_fees = cls.DELEGATE_FEE * sum((
            school.beginner_delegates,
            school.intermediate_delegates,
            school.advanced_delegates,
        ))
        school.fees_owed = cls.REGISTRATION_FEE + delegate_fees

    @classmethod
    def update_waitlist(cls, **kwargs):
        '''If the school is about to be created (i.e. has no ID) and
        registration is closed, add it to the waitlist.'''
        school = kwargs['instance']
        if not school.id and settings.CONFERENCE_WAITLIST_OPEN:
            school.waitlist = True

    @property
    def country_preference_ids(self):
        '''Return an ordered list of the school's preferred countries.'''
        return [country.id for country in self.countrypreferences.all()]

    @country_preference_ids.setter
    def country_preference_ids(self, country_ids):
        '''Queue a pending update to replace the school's preferred countries
        on the next save.'''
        self._pending_country_preference_ids = country_ids

    def save(self, *args, **kwargs):
        '''Save the school normally, then update its country preferences.'''
        super(School, self).save(*args, **kwargs)
        if getattr(self, '_pending_country_preference_ids', []):
            self.update_country_preferences(self._pending_country_preference_ids)
            self._pending_country_preference_ids = []

    @classmethod
    def email_comments(cls, **kwargs):
        school = kwargs['instance']
        if kwargs['created'] and school.registration_comments:
            send_mail('Registration Comments from '+ school.name, school.name +
                ' made comments about registration: '
                + school.registration_comments, 'tech@bmun.org',
                ['external@bmun.org'], fail_silently=True)

    @classmethod
    def email_confirmation(cls, **kwargs):
        if kwargs['created']:
            school = kwargs['instance']
            send_mail('BMUN 63 Registration Confirmation',
                      'You have officially been registered for BMUN 63. '
                      'To access your account, please log in at huxley.bmun.org.\n\n'
                      'The school registration fee is $50. The delegate registration '
                      'fee is $50 per student. You will be able to view your balance '
                      'on huxley.bmun.org in November, at which point we will begin '
                      'accepting payments.\n\n'
                      'If you have any tech related questions, please email tech@bmun.org. '
                      'For all other questions, please email info@bmun.org\n\n'
                      'Thank you for using Huxley!',
                      'no-reply@bmun.org',
                      [school.primary_email], fail_silently=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'school'

pre_save.connect(School.update_fees, sender=School)
pre_save.connect(School.update_waitlist, sender=School)
post_save.connect(School.email_comments, sender=School)
post_save.connect(School.email_confirmation, sender=School)


class Assignment(models.Model):
    committee = models.ForeignKey(Committee)
    country   = models.ForeignKey(Country)
    school    = models.ForeignKey(School, null=True, blank=True, default=None)

    @classmethod
    def update_assignments(cls, new_assignments):
        '''
        Atomically update the set of country assignments in a transaction.

        For each assignment in the updated list, either update the existing
        one (and delete its delegates), or create a new one if it doesn't
        exist.
        '''
        assignments = cls.objects.all().values()
        assignment_dict = {(a['committee_id'], a['country_id']): a
                           for a in assignments}
        additions = []
        deletions = []

        def add(committee, country, school):
            additions.append(cls(
                committee_id=committee,
                country_id=country,
                school_id=school,
            ))

        def remove(assignment_data):
            deletions.append(assignment_data['id'])

        for committee, country, school in new_assignments:
            key = (committee, country)
            old_assignment = assignment_dict.get(key)

            if not old_assignment:
                add(committee, country, school)
                continue

            if old_assignment['school_id'] != school:
                # Remove the old assignment instead of just updating it
                # so that its delegates are deleted by cascade.
                remove(old_assignment)
                add(committee, country, school)

            del assignment_dict[key]

        for old_assignment in assignment_dict.values():
            remove(old_assignment)

        with transaction.atomic():
            Assignment.objects.filter(id__in=deletions).delete()
            Assignment.objects.bulk_create(additions)

    def __unicode__(self):
        return self.committee.name + " : " + self.country.name + " : " + (self.school.name if self.school else "Unassigned")

    class Meta:
        db_table = u'assignment'
        unique_together = ('committee', 'country')


class CountryPreference(models.Model):
    school  = models.ForeignKey(School)
    country = models.ForeignKey(Country, limit_choices_to={'special': False})
    rank    = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return '%s : %s (%d)' % (self.school.name, self.country.name, self.rank)

    class Meta:
        db_table = u'country_preference'
        ordering = ['-school','rank']
        unique_together = ('country', 'school')


class Delegate(models.Model):
    assignment    = models.ForeignKey(Assignment, related_name='delegates')
    name          = models.CharField(max_length=64, blank=True)
    email         = models.EmailField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    summary       = models.TextField(default='', null=True)

    def __unicode__(self):
        return self.name

    @property
    def country(self):
        return self.assignment.country

    @property
    def committee(self):
        return self.assignment.committee

    @property
    def school(self):
        return self.assignment.school

    class Meta:
        db_table = u'delegate'
        ordering = ['assignment__country']
