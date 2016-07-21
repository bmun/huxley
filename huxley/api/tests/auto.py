# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.urlresolvers import resolve, reverse
from django.db import models
from rest_framework import serializers

from huxley.api.tests import DestroyAPITestCase, RetrieveAPITestCase


EXP_NOT_AUTHENTICATED = 'exp_not_authenticated'
EXP_PERMISSION_DENIED = 'exp_permission_denied'
EXP_DELETE_NOT_ALLOWED = 'exp_delete_not_allowed'


class AutoTestMixin(object):

    @classmethod
    def get_test_object(cls):
        raise NotImplementedError('You must provide a test object to retrieve.')

    @classmethod
    def get_view(cls):
        url_args = (1,) if cls.is_resource else ()
        return resolve(reverse(cls.url_name, args=url_args)).func.cls

    @classmethod
    def setUpTestData(cls):
        cls.object = cls.get_test_object()
        cls.view = cls.get_view()

    def do_test(self, username=None, password=None, expected_error=None):
        if username and password:
            self.client.login(username=username, password=password)
        response = self.get_response(self.object.id)

        self.assert_error(response, expected_error)
        self.assert_response(response, expected_error)

    def assert_response(self, response, expected_error):
        raise NotImplementedError('You must provide a method to test the response.')

    def assert_error(self, response, expected_error):
        if expected_error == EXP_NOT_AUTHENTICATED:
            self.assertNotAuthenticated(response)
        elif expected_error == EXP_PERMISSION_DENIED:
            self.assertPermissionDenied(response)
        elif expected_error == EXP_DELETE_NOT_ALLOWED:
            self.assertMethodNotAllowed(response, 'DELETE')


class RetrieveAPIAutoTestCase(AutoTestMixin, RetrieveAPITestCase):

    def assert_response(self, response, expected_error):
        if expected_error:
            return

        serializer = self.view.serializer_class
        expected_data = get_expected_data(
            serializer,
            serializer.Meta.model,
            self.object,
        )
        self.assertEqual(response.data, expected_data)


class DestroyAPIAutoTestCase(AutoTestMixin, DestroyAPITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.view = cls.get_view()

    def setUp(self):
        self.object = self.get_test_object()

    def assert_response(self, response, expected_error):
        object_exists = self.view.queryset.filter(id=self.object.id).exists()
        if expected_error:
            self.assertTrue(object_exists)
        else:
            self.assertEqual(response.data, None)
            self.assertFalse(object_exists)


def get_expected_data(serializer, model, test_object):
    serializer_fields = serializer._declared_fields
    expected_data = {}
    for field_name in serializer.Meta.fields:
        expected_data[field_name] = transform_attr(
            getattr(test_object, field_name),
            test_object,
            model._meta.get_field(field_name),
            serializer_fields.get(field_name, None),
        )

    return expected_data


def transform_attr(attr, test_object, model_field, serializer_field):
    if isinstance(model_field, models.DecimalField):
        return float(attr)
    if isinstance(model_field, models.DateTimeField):
        return attr.isoformat()
    if isinstance(model_field, models.ForeignKey):
        return attr.pk

    if not serializer_field:
        return attr

    if isinstance(serializer_field, serializers.DateTimeField):
        return attr.isoformat()
    if isinstance(serializer_field, serializers.ListField):
        return list(getattr(test_object, serializer_field.source))
    if isinstance(serializer_field, serializers.ManyRelatedField):
        return list(attr.all())

    return attr
