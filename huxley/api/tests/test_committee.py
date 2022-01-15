# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).
from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models


class CommitteeDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:committee_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_committee()

    def test_anonymous_user(self):
        self.do_test()


class CommitteeDetailPutTestCase(tests.UpdateAPITestCase):
    url_name = 'api:committee_detail'
    params = {'name': 'DISC', 'special': True}

    def setUp(self):
        self.chair = models.new_user(username='chair',
                                     password='chair',
                                     user_type=User.TYPE_CHAIR)
        self.committee = models.new_committee(user=self.chair)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update committees.'''
        response = self.get_response(self.committee.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_delegate(self):
        '''Delegates shouldn't be able to update committees.'''
        models.new_user(username='delegate',
                        password='user',
                        user_type=User.TYPE_DELEGATE)
        self.client.login(username='delegate', password='user')

        response = self.get_response(self.committee.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_advisor(self):
        '''Advisors shouldn't be able to update committees.'''
        models.new_user(username='advisor',
                        password='user',
                        user_type=User.TYPE_ADVISOR)
        self.client.login(username='advisor', password='user')

        response = self.get_response(self.committee.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''Chairs should be able to update committees.'''
        self.client.login(username='chair', password='chair')

        response = self.get_response(self.committee.id, params=self.params)
        response.data.pop('rubric')
        self.assertEqual(
            response.data, {
                'id': self.committee.id,
                'name': 'DISC',
                'full_name': self.committee.full_name,
                'delegation_size': self.committee.delegation_size,
                'special': True,
                'notes_activated': self.committee.notes_activated,
                'zoom_link': self.committee.zoom_link
            })

    def test_superuser(self):
        '''Superusers shouldn't be able to update committees.'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.committee.id, params=self.params)
        response.data.pop('rubric')
        self.assertEqual(
            response.data, {
                'id': self.committee.id,
                'name': 'DISC',
                'full_name': self.committee.full_name,
                'delegation_size': self.committee.delegation_size,
                'special': True,
                'notes_activated': self.committee.notes_activated,
                'zoom_link': self.committee.zoom_link
            })


class CommitteeDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:committee_detail'
    params = {'name': 'DISC', 'special': True}

    def setUp(self):
        self.chair = models.new_user(username='chair',
                                     password='chair',
                                     user_type=User.TYPE_CHAIR)
        self.committee = models.new_committee(user=self.chair)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update committees.'''
        response = self.get_response(self.committee.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_delegate(self):
        '''Delegates shouldn't be able to update committees.'''
        models.new_user(username='delegate',
                        password='user',
                        user_type=User.TYPE_DELEGATE)
        self.client.login(username='delegate', password='user')

        response = self.get_response(self.committee.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_advisor(self):
        '''Advisors shouldn't be able to update committees.'''
        models.new_user(username='advisor',
                        password='user',
                        user_type=User.TYPE_ADVISOR)
        self.client.login(username='advisor', password='user')

        response = self.get_response(self.committee.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''Chairs should be able to update committees.'''
        self.client.login(username='chair', password='chair')

        response = self.get_response(self.committee.id, params=self.params)
        response.data.pop('rubric')
        self.assertEqual(
            response.data, {
                'id': self.committee.id,
                'name': 'DISC',
                'full_name': self.committee.full_name,
                'delegation_size': self.committee.delegation_size,
                'special': True,
                'notes_activated': self.committee.notes_activated,
                'zoom_link': self.committee.zoom_link
            })

    def test_superuser(self):
        '''Superusers shouldn't be able to update committees.'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.committee.id, params=self.params)
        response.data.pop('rubric')
        self.assertEqual(
            response.data, {
                'id': self.committee.id,
                'name': 'DISC',
                'full_name': self.committee.full_name,
                'delegation_size': self.committee.delegation_size,
                'special': True,
                'notes_activated': self.committee.notes_activated,
                'zoom_link': self.committee.zoom_link
            })


class CommitteeDetailDeleteTestCase(auto.DestroyAPIAutoTestCase):
    url_name = 'api:committee_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_committee()

    def test_anonymous_user(self):
        '''Anonymous users cannot delete committees.'''
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_authenticated_user(self):
        '''Authenticated users cannot delete committees.'''
        self.as_default_user().do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

    def test_superuser(self):
        '''Superusers cannot delete committees.'''
        self.as_superuser().do_test(expected_error=auto.EXP_DELETE_NOT_ALLOWED)


class CommitteeListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:committee_list'

    def test_anonymous_user(self):
        '''Anyone should be able to access a list of all the committees.'''
        c1 = models.new_committee(name='DISC', delegation_size=100)
        c2 = models.new_committee(name='JCC', special=True, delegation_size=30)

        response = self.get_response()
        for r in response.data:
            r.pop('rubric')
        self.assertEqual(response.data, [{
            'delegation_size': c1.delegation_size,
            'special': c1.special,
            'id': c1.id,
            'full_name': c1.full_name,
            'name': c1.name,
            'notes_activated': c1.notes_activated,
            'zoom_link': c1.zoom_link
        }, {
            'delegation_size': c2.delegation_size,
            'special': c2.special,
            'id': c2.id,
            'full_name': c2.full_name,
            'name': c2.name,
            'notes_activated': c2.notes_activated,
            'zoom_link': c2.zoom_link
        }])


class CommitteeListPostTestCase(tests.CreateAPITestCase):
    url_name = 'api:committee_list'
    params = {
        'name': 'DISC',
        'full_name': 'Disarmament and International Security',
        'delegation_size': 100
    }

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to create committees.'''
        response = self.get_response(self.params)
        self.assertMethodNotAllowed(response, 'POST')

    def test_authenticated_user(self):
        '''Authenticated users shouldn't be able to create committees.'''
        models.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.params)
        self.assertMethodNotAllowed(response, 'POST')

    def test_superuser(self):
        '''Superusers shouldn't be able to create committees.'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.params)
        self.assertMethodNotAllowed(response, 'POST')
