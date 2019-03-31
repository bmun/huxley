# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json
import requests

import os

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models, transaction
from django.db.models.signals import post_init, post_save, pre_delete, pre_save
from django.utils import timezone

from huxley.core.constants import ContactGender, ContactType, ProgramTypes


class Conference(models.Model):
    session = models.PositiveSmallIntegerField(default=0, primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reg_open = models.DateField()
    early_reg_close = models.DateField()
    reg_close = models.DateField()
    min_attendance = models.PositiveSmallIntegerField(default=0)
    max_attendance = models.PositiveSmallIntegerField(default=0)
    open_reg = models.BooleanField(default=True)
    waitlist_reg = models.BooleanField(default=False)
    position_papers_accepted = models.BooleanField(default=False)
    external = models.CharField(max_length=128)
    registration_fee = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal('50.00'))
    delegate_fee = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal('50.00'))

    @classmethod
    def get_current(cls):
        return Conference.objects.get(session=settings.SESSION)

    def __unicode__(self):
        return 'BMUN %d' % self.session

    class Meta:
        db_table = u'conference'
        get_latest_by = 'start_date'


class Country(models.Model):
    name = models.CharField(max_length=128)
    special = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'country'


class Rubric(models.Model):
    topic_one = models.CharField(max_length=64, default='', blank=True)
    grade_category_1 = models.CharField(max_length=128, default='', blank=True)
    grade_category_2 = models.CharField(max_length=128, default='', blank=True)
    grade_category_3 = models.CharField(max_length=128, default='', blank=True)
    grade_category_4 = models.CharField(max_length=128, default='', blank=True)
    grade_category_5 = models.CharField(max_length=128, default='', blank=True)

    grade_value_1 = models.PositiveSmallIntegerField(default=10)
    grade_value_2 = models.PositiveSmallIntegerField(default=10)
    grade_value_3 = models.PositiveSmallIntegerField(default=10)
    grade_value_4 = models.PositiveSmallIntegerField(default=10)
    grade_value_5 = models.PositiveSmallIntegerField(default=10)

    # Values below this for the second paper topic
    topic_two = models.CharField(max_length=64, default='', blank=True)
    use_topic_2 = models.BooleanField(default=True)
    grade_t2_category_1 = models.CharField(
        max_length=128, default='', blank=True)
    grade_t2_category_2 = models.CharField(
        max_length=128, default='', blank=True)
    grade_t2_category_3 = models.CharField(
        max_length=128, default='', blank=True)
    grade_t2_category_4 = models.CharField(
        max_length=128, default='', blank=True)
    grade_t2_category_5 = models.CharField(
        max_length=128, default='', blank=True)

    grade_t2_value_1 = models.PositiveSmallIntegerField(default=10)
    grade_t2_value_2 = models.PositiveSmallIntegerField(default=10)
    grade_t2_value_3 = models.PositiveSmallIntegerField(default=10)
    grade_t2_value_4 = models.PositiveSmallIntegerField(default=10)
    grade_t2_value_5 = models.PositiveSmallIntegerField(default=10)

    def __unicode__(self):
        return '%s' % self.committee.name if self.committee else '%d' % self.id

    class Meta:
        db_table = u'rubric'


class Committee(models.Model):
    name = models.CharField(max_length=8)
    full_name = models.CharField(max_length=128)
    countries = models.ManyToManyField(Country, through='Assignment')
    delegation_size = models.PositiveSmallIntegerField(default=2)
    special = models.BooleanField(default=False)
    rubric = models.OneToOneField(Rubric, blank=True, null=True)

    @classmethod
    def create_rubric(cls, **kwargs):
        committee = kwargs['instance']
        if not committee.rubric:
            committee.rubric = Rubric.objects.create()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'committee'


class CommitteeFeedback(models.Model):
    CHOICES = ((0, 0),
               (1, 1),
               (2, 2),
               (3, 3),
               (4, 4),
               (5, 5),
               (6, 6),
               (7, 7),
               (8, 8),
               (9, 9),
               (10, 10), )

    committee = models.ForeignKey(Committee)
    comment = models.TextField(blank=True, default='')
    rating = models.IntegerField(blank=True, default=0, choices=CHOICES)

    chair_1_name = models.CharField(blank=True, default='', max_length=100)
    chair_2_name = models.CharField(blank=True, default='', max_length=100)
    chair_3_name = models.CharField(blank=True, default='', max_length=100)
    chair_4_name = models.CharField(blank=True, default='', max_length=100)
    chair_5_name = models.CharField(blank=True, default='', max_length=100)
    chair_6_name = models.CharField(blank=True, default='', max_length=100)
    chair_7_name = models.CharField(blank=True, default='', max_length=100)
    chair_8_name = models.CharField(blank=True, default='', max_length=100)
    chair_9_name = models.CharField(blank=True, default='', max_length=100)
    chair_10_name = models.CharField(blank=True, default='', max_length=100)

    chair_1_comment = models.TextField(blank=True, default='')
    chair_2_comment = models.TextField(blank=True, default='')
    chair_3_comment = models.TextField(blank=True, default='')
    chair_4_comment = models.TextField(blank=True, default='')
    chair_5_comment = models.TextField(blank=True, default='')
    chair_6_comment = models.TextField(blank=True, default='')
    chair_7_comment = models.TextField(blank=True, default='')
    chair_8_comment = models.TextField(blank=True, default='')
    chair_9_comment = models.TextField(blank=True, default='')
    chair_10_comment = models.TextField(blank=True, default='')

    chair_1_rating = models.IntegerField(
        blank=True, default=0, choices=CHOICES)
    chair_2_rating = models.IntegerField(
        blank=True, default=0, choices=CHOICES)
    chair_3_rating = models.IntegerField(
        blank=True, default=0, choices=CHOICES)
    chair_4_rating = models.IntegerField(
        blank=True, default=0, choices=CHOICES)
    chair_5_rating = models.IntegerField(
        blank=True, default=0, choices=CHOICES)
    chair_6_rating = models.IntegerField(
        blank=True, default=0, choices=CHOICES)
    chair_7_rating = models.IntegerField(
        blank=True, default=0, choices=CHOICES)
    chair_8_rating = models.IntegerField(
        blank=True, default=0, choices=CHOICES)
    chair_9_rating = models.IntegerField(
        blank=True, default=0, choices=CHOICES)
    chair_10_rating = models.IntegerField(
        blank=True, default=0, choices=CHOICES)

    def __unicode__(self):
        return str(self.committee.name) + " - Comment " + str(self.id)

    class Meta:
        db_table = u'committee_feedback'


pre_save.connect(Committee.create_rubric, sender=Committee)

class Speech(models.Model):
    pass

class InCommitteeFeedback(models.Model):
    feedback = models.TextField()
    assignment = models.ForeignKey(Assignment)
    speech = models.OneToOneField('Speech', blank=True, null=True)
    score = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        a = self.assignment
        return '%s %s Feedback %d' % (a.committee.name, a.country.name,
                             self.id) if a else 'Feedback %d' % (self.id)

    class Meta:
        db_table = u'in_committee_feedback'

class School(models.Model):
    PROGRAM_TYPE_OPTIONS = ((ProgramTypes.CLUB, 'Club'),
                            (ProgramTypes.CLASS, 'Class'), )

    CONTACT_TYPE_OPTIONS = ((ContactType.FACULTY, 'Faculty'),
                            (ContactType.STUDENT, 'Student'), )

    GENDER_OPTIONS = ((ContactGender.MALE, 'Male'),
                      (ContactGender.FEMALE, 'Female'),
                      (ContactGender.OTHER, 'Other'),
                      (ContactGender.UNSPECIFIED, 'Unspecified'), )

    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=16)
    zip_code = models.CharField(max_length=16)
    country = models.CharField(max_length=64)
    primary_name = models.CharField(max_length=128)
    primary_gender = models.PositiveSmallIntegerField(
        choices=GENDER_OPTIONS, default=ContactGender.UNSPECIFIED)
    primary_email = models.EmailField()
    primary_phone = models.CharField(max_length=32)
    primary_type = models.PositiveSmallIntegerField(
        choices=CONTACT_TYPE_OPTIONS, default=ContactType.FACULTY)
    secondary_name = models.CharField(max_length=128, blank=True)
    secondary_gender = models.PositiveSmallIntegerField(
        choices=GENDER_OPTIONS, blank=True, default=ContactGender.UNSPECIFIED)
    secondary_email = models.EmailField(blank=True)
    secondary_phone = models.CharField(max_length=32, blank=True)
    secondary_type = models.PositiveSmallIntegerField(
        choices=CONTACT_TYPE_OPTIONS, blank=True, default=ContactType.FACULTY)
    program_type = models.PositiveSmallIntegerField(
        choices=PROGRAM_TYPE_OPTIONS, default=ProgramTypes.CLUB)
    times_attended = models.PositiveSmallIntegerField(default=0)
    international = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'school'


class Registration(models.Model):
    school = models.ForeignKey(School, related_name='registrations')
    conference = models.ForeignKey(Conference, related_name='registrations')

    registered_at = models.DateTimeField(auto_now_add=True)

    num_beginner_delegates = models.PositiveSmallIntegerField()
    num_intermediate_delegates = models.PositiveSmallIntegerField()
    num_advanced_delegates = models.PositiveSmallIntegerField()
    num_spanish_speaking_delegates = models.PositiveSmallIntegerField()
    num_chinese_speaking_delegates = models.PositiveSmallIntegerField()

    country_preferences = models.ManyToManyField(
        Country, through='CountryPreference')
    committee_preferences = models.ManyToManyField(Committee, blank=True)

    registration_comments = models.TextField(default='', blank=True)

    is_waitlisted = models.BooleanField(default=False)
    waivers_completed = models.BooleanField(default=False)

    assignments_finalized = models.BooleanField(default=False)

    delegate_fees_owed = models.DecimalField(
        max_digits=7, decimal_places=2, default=Decimal('0.00'))
    delegate_fees_paid = models.DecimalField(
        max_digits=7, decimal_places=2, default=Decimal('0.00'))
    registration_fee_paid = models.BooleanField(default=False)

    modified_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def update_fees(cls, **kwargs):
        registration = kwargs['instance']
        delegate_fee = Conference.get_current().delegate_fee
        delegate_fees = delegate_fee * sum(
            (registration.num_beginner_delegates,
             registration.num_intermediate_delegates,
             registration.num_advanced_delegates, ))
        registration.delegate_fees_owed = Decimal(delegate_fees) + Decimal(
            '0.00')

    @classmethod
    def update_waitlist(cls, **kwargs):
        '''If the registration is about to be created (i.e. has no ID) and
        registration is closed, add it to the waitlist.'''
        registration = kwargs['instance']
        conference = Conference.get_current()
        if not registration.id and conference.waitlist_reg:
            registration.is_waitlisted = True

    @classmethod
    def email_comments(cls, **kwargs):
        registration = kwargs['instance']
        if kwargs['created'] and registration.registration_comments:
            send_mail(
                'Registration Comments from ' + registration.school.name,
                registration.school.name +
                ' made comments about registration: ' +
                registration.registration_comments,
                'tech@bmun.org', ['info@bmun.org'],
                fail_silently=False)

    @classmethod
    def email_confirmation(cls, **kwargs):
        conference = Conference.get_current()
        if kwargs['created']:
            registration = kwargs['instance']
            if registration.is_waitlisted:
                send_mail(
                    'BMUN %d Waitlist Confirmation' % conference.session,
                    'You have officially been put on the waitlist for BMUN %d. '
                    'We will inform you if and when you are taken off the waitlist.\n\n'
                    'If you have any tech related questions, please email tech@bmun.org. '
                    'For all other questions, please email info@bmun.org.\n\n'
                    'Thank you for using Huxley!' % conference.session,
                    'no-reply@bmun.org', [registration.school.primary_email],
                    fail_silently=False)
            else:
                registration_fee = conference.registration_fee
                delegate_fee = conference.delegate_fee
                send_mail(
                    'BMUN %d Registration Confirmation' % conference.session,
                    'Congratulations, you have officially been registered for BMUN %d. '
                    'To access your account, please log in at huxley.bmun.org.\n\n'
                    'In order to confirm your spot on our registration list, '
                    'you must pay the non-refundable school fee of $%d. '
                    'In 24-48 hours, you will receive an invoice from QuickBooks, '
                    'our accounting system, for your school fee. '
                    'You can either pay online through the QuickBooks payment portal '
                    'or mail a check to the address listed on the invoice. '
                    'More information on payment methods and deadlines can be found '
                    'in the invoice or at http://www.bmun.org/conference-fees/. '
                    'If you do not pay by the deadline, then you will be dropped to our waitlist.\n\n'
                    'In addition to the school fee, there is also a delegate fee of $%d per student. '
                    'The invoice for this will be sent out with country assignments '
                    'shortly after that.\n\n'
                    'If you have any students that need financial assistance, '
                    'we encourage them to apply for our Alumni Scholarship '
                    'at http://bmun.org/alumni-scholarship/.\n\n'
                    'If you have any questions, please contact info@bmun.org.\n\n'
                    'Thank you for registering for BMUN, and we look forward to '
                    'seeing you at the oldest high school conference in the world '
                    'on March 1-3, 2019.' %
                    (conference.session, int(registration_fee),
                     int(delegate_fee)),
                    'no-reply@bmun.org', [registration.school.primary_email],
                    fail_silently=False)

    @property
    def country_preference_ids(self):
        '''Return an ordered list of the registration's preferred countries.'''
        return [country.id
                for country in self.country_preferences.all().order_by(
                    'countrypreference')]

    @country_preference_ids.setter
    def country_preference_ids(self, country_ids):
        '''Queue a pending update to replace the registration's preferred countries
        on the next save.'''
        self._pending_country_preference_ids = country_ids

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
                    registration=self,
                    country_id=country_id,
                    rank=rank, ))

        if country_preferences:
            with transaction.atomic():
                self.country_preferences.clear()
                CountryPreference.objects.bulk_create(country_preferences)

        return processed_country_ids

    def save(self, *args, **kwargs):
        '''Save the registration normally, then update its country preferences.'''
        super(Registration, self).save(*args, **kwargs)
        if getattr(self, '_pending_country_preference_ids', []):
            self.update_country_preferences(
                self._pending_country_preference_ids)
            self._pending_country_preference_ids = []

    def __unicode__(self):
        return self.school.name + ' - ' + str(self.conference.session)

    class Meta:
        db_table = u'registration'
        unique_together = ('conference', 'school')


pre_save.connect(Registration.update_fees, sender=Registration)
pre_save.connect(Registration.update_waitlist, sender=Registration)
post_save.connect(Registration.email_comments, sender=Registration)
post_save.connect(Registration.email_confirmation, sender=Registration)


class PositionPaper(models.Model):
    file = models.FileField(upload_to="position_papers/", null=True)
    graded_file = models.FileField(
        upload_to="graded_papers/", null=True, blank=True)
    graded = models.BooleanField(default=False)
    score_1 = models.PositiveSmallIntegerField(default=0)
    score_2 = models.PositiveSmallIntegerField(default=0)
    score_3 = models.PositiveSmallIntegerField(default=0)
    score_4 = models.PositiveSmallIntegerField(default=0)
    score_5 = models.PositiveSmallIntegerField(default=0)

    # Scores below this for the second paper topic
    # Only used for committees with two topics
    score_t2_1 = models.PositiveSmallIntegerField(default=0)
    score_t2_2 = models.PositiveSmallIntegerField(default=0)
    score_t2_3 = models.PositiveSmallIntegerField(default=0)
    score_t2_4 = models.PositiveSmallIntegerField(default=0)
    score_t2_5 = models.PositiveSmallIntegerField(default=0)

    submission_date = models.DateField(null=True)

    @classmethod
    def delete_prev_file(cls, **kwargs):
        position_paper = kwargs['instance']
        if hasattr(position_paper, '_prev_file') and \
           position_paper.file.name != position_paper._prev_file and \
           os.path.isfile(position_paper._prev_file):
            os.remove(position_paper._prev_file)

    @classmethod
    def store_file_path(cls, **kwargs):
        position_paper = kwargs['instance']
        position_paper._prev_file = position_paper.file.name

    def __unicode__(self):
        a = self.assignment
        return '%s %s %d' % (a.committee.name, a.country.name,
                             a.id) if a else '%d' % (self.id)

    class Meta:
        db_table = u'position_papers'


post_init.connect(PositionPaper.store_file_path, sender=PositionPaper)
post_save.connect(PositionPaper.delete_prev_file, sender=PositionPaper)


class Assignment(models.Model):
    committee = models.ForeignKey(Committee)
    country = models.ForeignKey(Country)
    registration = models.ForeignKey(Registration, null=True)
    rejected = models.BooleanField(default=False)
    paper = models.OneToOneField(PositionPaper, blank=True, null=True)

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
        assigned = dict()
        failed_assignments = []

        def add(committee, country, registration, paper, rejected):
            additions.append(
                cls(committee_id=committee.id,
                    country_id=country.id,
                    registration_id=registration.id,
                    paper_id=paper.id,
                    rejected=rejected, ))

        def remove(assignment_data):
            deletions.append(assignment_data['id'])

        for committee, country, school, rejected in new_assignments:
            # If the assignemnt contains no bad cells, then each value should
            # have the type of its corresponding model.
            is_invalid = False
            if type(committee) is not Committee:
                committee = Committee(name=committee + ' - DOES NOT EXIST')
                is_invalid = True
            if type(country) is not Country:
                country = Country(name=country + ' - DOES NOT EXIST')
                is_invalid = True
            if type(school) is not School:
                school = School(name=school + ' - DOES NOT EXIST')
                is_invalid = True
            else:
                try:
                    registration = Registration.objects.get(
                        school_id=school.id)
                except Registration.DoesNotExist:
                    is_invalid = True

            if is_invalid:
                failed_assignments.append(
                    str((str(school.name), str(committee.name), str(
                        country.name))))
                continue

            key = (committee.id, country.id)
            if key in assigned.keys():
                # Make sure that the same committee/country pair is not being
                # given to more than one school in the upload
                if assigned[key] == school.id:
                    continue
                committee = str(committee.name)
                country = str(country.name)
                failed_assignments.append(
                    str((committee, country)) +
                    ' - ASSIGNED TO MORE THAN ONE SCHOOL')
                continue

            assigned[key] = school.id
            old_assignment = assignment_dict.get(key)
            paper = PositionPaper.objects.create()
            paper.save()

            if not old_assignment:
                add(committee, country, registration, paper, rejected)
                continue

            if old_assignment['registration_id'] != registration:
                # Remove the old assignment instead of just updating it
                # so that its delegates are deleted by cascade.
                remove(old_assignment)
                add(committee, country, registration, paper, rejected)

        if not failed_assignments:
            with transaction.atomic():
                Assignment.objects.filter(id__in=deletions).delete()
                Assignment.objects.bulk_create(additions)

        return failed_assignments

    @classmethod
    def update_assignment(cls, **kwargs):
        '''Ensures that when an assignment's school field changes,
           any delegates assigned to that assignment are no longer
           assigned to it and that its rejected field is false.'''
        assignment = kwargs['instance']
        if not assignment.id:
            return

        old_assignment = cls.objects.get(id=assignment.id)
        if assignment.registration_id != old_assignment.registration_id:
            assignment.rejected = False
            Delegate.objects.filter(assignment_id=old_assignment.id).update(
                assignment=None)

    @classmethod
    def create_position_paper(cls, **kwargs):
        assignment = kwargs['instance']
        if not assignment.paper:
            assignment.paper = PositionPaper.objects.create()

    def __unicode__(self):
        return self.committee.name + " : " + self.country.name + " : " + (
            self.registration.school.name
            if self.registration else "Unassigned")

    class Meta:
        db_table = u'assignment'
        unique_together = ('committee', 'country')


pre_save.connect(Assignment.update_assignment, sender=Assignment)
pre_save.connect(Assignment.create_position_paper, sender=Assignment)


class CountryPreference(models.Model):
    registration = models.ForeignKey(Registration, null=True)
    country = models.ForeignKey(Country, limit_choices_to={'special': False})
    rank = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return '%s : %s (%d)' % (self.registration.school.name,
                                 self.country.name, self.rank)

    class Meta:
        db_table = u'country_preference'
        ordering = ['-registration', 'rank']
        unique_together = ('country', 'registration')


class Delegate(models.Model):
    school = models.ForeignKey(School, related_name='delegates', null=True)
    assignment = models.ForeignKey(
        Assignment,
        related_name='delegates',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    name = models.CharField(max_length=64)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(default='', blank=True, null=True)
    published_summary = models.TextField(default='', blank=True, null=True)

    voting = models.BooleanField(default=False)
    session_one = models.BooleanField(default=False)
    session_two = models.BooleanField(default=False)
    session_three = models.BooleanField(default=False)
    session_four = models.BooleanField(default=False)

    committee_feedback_submitted = models.BooleanField(default=False)
    waiver_submitted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @property
    def country(self):
        if self.assignment:
            return self.assignment.country

        return None

    @property
    def committee(self):
        if self.assignment:
            return self.assignment.committee

        return None

    def save(self, *args, **kwargs):
        if (self.assignment_id and self.school_id and
                self.school_id != self.assignment.registration.school_id):
            raise ValidationError(
                'Delegate school and delegate assignment school do not match.')

        super(Delegate, self).save(*args, **kwargs)

    class Meta:
        db_table = u'delegate'
        ordering = ['school']


class SecretariatMember(models.Model):
    # A lot more could be added here but this is a good start

    name = models.CharField(blank=False, default='', max_length=100)
    committee = models.ForeignKey(Committee)
    is_head_chair = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
