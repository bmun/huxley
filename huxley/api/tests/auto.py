# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.db import models
from rest_framework import serializers

from huxley.api.tests import RetrieveAPITestCase


class RetrieveAPIAutoTestCase(RetrieveAPITestCase):
    NOT_AUTHENTICATED = 'not_authenticated'

    @classmethod
    def get_test_object(cls):
        raise NotImplementedError('You must provide a test object to retrieve.')

    @classmethod
    def get_users(cls, obj):
        raise NotImplementedError('You must provide test users.')

    @classmethod
    def setUpTestData(cls):
        cls.object = cls.get_test_object()
        cls.users = cls.get_users(cls.object)

    def test(self):
        for user_data in self.users:
            username, password, expected_error = user_data
            if username and password:
                self.client.login(username=username, password=password)
            response = self.get_response(self.object.id)

            if expected_error == self.NOT_AUTHENTICATED:
                self.assertNotAuthenticated(response)
            else:
                self.assert_response(response)

    def assert_response(self, response):
        serializer = self.view.serializer_class
        expected_response = get_expected_response(
            serializer,
            serializer.Meta.model,
            self.object,
        )
        self.assertEqual(response.data, expected_response)


def get_expected_response(serializer, model, test_object):
    serializer_fields = serializer._declared_fields
    expected = {}
    for field_name in serializer.Meta.fields:
        field = model._meta.get_field(field_name)
        attr = getattr(test_object, field_name)

        if isinstance(field, models.DecimalField):
            attr = float(attr)

        serializer_field = serializer_fields.get(field_name, None)
        if serializer_field:
            if isinstance(serializer_field, serializers.DateTimeField):
                attr = attr.isoformat()
            elif isinstance(serializer_field, serializers.ListField):
                attr = list(getattr(test_object, serializer_field.source))
            elif isinstance(serializer_field, serializers.ManyRelatedField):
                attr = list(attr.all())

        expected[field_name] = attr

    return expected
