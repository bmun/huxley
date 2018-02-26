# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class AbstractAPITestCase(APITestCase):
    '''Provides a base implementation to test REST APIs, with concrete
    children for each of the REST methods.

    Classes that extend the concrete children ust define a url_name class
    member, and can then use the get_response() method to make a request.

    They can optionally specify a params class member to define default
    params and then use get_params() to override certain properties.'''

    fixtures = ['conference']
    url_name = None
    params = {}
    method = None
    is_resource = None

    def get_url(self, object_id=None):
        if self.url_name is None:
            raise NotImplementedError('Must define url_name class member.')
        if self.is_resource is None:
            raise NotImplementedError('Must define is_resource class member.')

        args = None
        if self.is_resource:
            args = (object_id, )
        else:
            args = ()

        return reverse(self.url_name, args=args)

    def get_params(self, **kwargs):
        params = self.params.copy()
        for param, value in kwargs.items():
            params[param] = value
        return params

    def get_response(self, object_id=None, params=None):
        if self.method is None:
            raise NotImplementedError('Must define method class member.')

        params = params or self.params
        if self.method != 'get':
            params = json.dumps(params)
        request = getattr(self.client, self.method)
        url = self.get_url(object_id)
        return request(url, params, content_type='application/json')

    def assertOK(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def assert204(self, response):
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def assertPermissionDenied(self, response):
        self.assertEqual(response.data, {
            'detail': u'You do not have permission to perform this action.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertMethodNotAllowed(self, response, method):
        self.assertEqual(response.data, {
            u'detail': u'Method "%s" not allowed.' % method
        })
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def assertNotAuthenticated(self, response):
        self.assertEqual(response.data, {
            'detail': u'Authentication credentials were not provided.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertAuthenticationFailed(self, response):
        self.assertEqual(response.data, {
            'detail': u'Incorrect authentication credentials.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertNotFound(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assertInvalidCharacters(self, response, field):
        self.assertEqual(response.data, {
            '%s' % field: [u'This field contains invalid characters.']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertInvalidEmail(self, response, field):
        self.assertEqual(response.data, {
            '%s' % field: [u'This is an invalid email address.']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertInvalidEmailFormat(self, response, field):
        self.assertEqual(response.data, {
            '%s' % field: [u'Enter a valid email address.']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertInvalidPhone(self, response, field):
        self.assertEqual(response.data, {
            '%s' % field: [u'This is an invalid phone number.']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertInvalidCommitteeRating(self, response, fields, data):
        for field in fields:
            self.assertEqual(
                response.data.get(field),
                [u'"' + str(data[field]) + '" is not a valid choice.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateAPITestCase(AbstractAPITestCase):
    method = 'post'
    is_resource = False


class ListAPITestCase(AbstractAPITestCase):
    method = 'get'
    is_resource = False


class RetrieveAPITestCase(AbstractAPITestCase):
    method = 'get'
    is_resource = True


class UpdateAPITestCase(AbstractAPITestCase):
    method = 'put'
    is_resource = True


class PartialUpdateAPITestCase(AbstractAPITestCase):
    method = 'patch'
    is_resource = True


class DestroyAPITestCase(AbstractAPITestCase):
    method = 'delete'
    is_resource = True
