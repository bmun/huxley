# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import collections

from huxley.accounts.models import User
from huxley.api import tests
from huxley.core.constants import ContactGender, ContactType, ProgramTypes
from huxley.core.models import Registration, School


class RegisterTestCase(tests.CreateAPITestCase):
    url_name = 'api:register'

    def test_valid(self):
        params = {
            'user': {
                'first_name': 'Trevor',
                'last_name': 'Dowds',
                'username': 'tdowds',
                'email': 'tdowds@huxley.org',
                'password': 'password',
                'school': {
                    'name': 'The Trevor School',
                    'address': '123 School Way',
                    'city': 'School City',
                    'state': 'CA',
                    'zip_code': '12345',
                    'country': 'USA',
                    'international': False,
                    'program_type': ProgramTypes.CLUB,
                    'times_attended': 0,
                    'primary_name': 'Trevor Dowds',
                    'primary_gender': ContactGender.MALE,
                    'primary_email': 'tdowds@huxley.org',
                    'primary_phone': '(999) 999-9999',
                    'primary_type': ContactType.FACULTY,
                    'secondary_name': '',
                    'secondary_gender': ContactGender.MALE,
                    'secondary_email': '',
                    'secondary_phone': '',
                    'secondary_type': ContactType.FACULTY,
                },
            },
            'registration': {
                'conference': 65,
                'num_beginner_delegates': 1,
                'num_intermediate_delegates': 0,
                'num_advanced_delegates': 0,
                'num_spanish_speaking_delegates': 0,
                'num_chinese_speaking_delegates': 0,
            }
        }

        response = self.get_response(params=params)
        user_query = User.objects.filter(id=response.data['user']['id'])
        self.assertTrue(user_query.exists())
        school_query = School.objects.filter(id=response.data['user']['school']['id'])
        self.assertTrue(school_query.exists())
        registration_query = Registration.objects.filter(id=response.data['registration']['id'])
        self.assertTrue(registration_query.exists())

        user = User.objects.get(id=response.data['user']['id'])
        school = School.objects.get(id=user.school_id)
        registration = Registration.objects.get(id=response.data['registration']['id'])
        response.data['user']['school'] = dict(response.data['user']['school'])
        self.assertEqual(response.data, {
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type,
                'school': {
                    'id': school.id,
                    'name': school.name,
                    'address': school.address,
                    'city': school.city,
                    'state': school.state,
                    'zip_code': school.zip_code,
                    'country': school.country,
                    'international': school.international,
                    'program_type': school.program_type,
                    'times_attended': school.times_attended,
                    'primary_name': school.primary_name,
                    'primary_gender': school.primary_gender,
                    'primary_email': school.primary_email,
                    'primary_phone': school.primary_phone,
                    'primary_type': school.primary_type,
                    'secondary_name': school.secondary_name,
                    'secondary_gender': school.secondary_gender,
                    'secondary_email': school.secondary_email,
                    'secondary_phone': school.secondary_phone,
                    'secondary_type': school.secondary_type
                }
            },
            'registration': {
                'id': registration.id,
                'conference': registration.conference.session,
                'school': registration.school_id,
                'registered_at': registration.registered_at.isoformat(),
                'num_beginner_delegates': registration.num_beginner_delegates,
                'num_intermediate_delegates': registration.num_intermediate_delegates,
                'num_advanced_delegates': registration.num_advanced_delegates,
                'num_spanish_speaking_delegates': registration.num_spanish_speaking_delegates,
                'num_chinese_speaking_delegates': registration.num_chinese_speaking_delegates,
                'country_preferences': registration.country_preference_ids,
                'committee_preferences': list(registration.committee_preferences.all()),
                'registration_comments': registration.registration_comments,
                'is_waitlisted': registration.is_waitlisted,
                'waivers_completed': registration.waivers_completed,
                'assignments_finalized': registration.assignments_finalized,
                'fees_paid': float(registration.fees_paid),
                'fees_owed': float(registration.fees_owed),
                'modified_at': registration.modified_at.isoformat()
            }
        })
