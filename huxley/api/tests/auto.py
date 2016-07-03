# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from collections import namedtuple

from django.db import models
from rest_framework import serializers

from huxley.api.tests import RetrieveAPITestCase


User = namedtuple('User', ['username', 'password', 'expected_error'])
User.__new__.__defaults__ = (None, None, None)


EXP_NOT_AUTHENTICATED = 'exp_not_authenticated'


class RetrieveAPIAutoTestCase(RetrieveAPITestCase):

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

            if expected_error == EXP_NOT_AUTHENTICATED:
                self.assertNotAuthenticated(response)
            else:
                self.assert_response(response)

    def assert_response(self, response):
        serializer = self.view.serializer_class
        expected_data = get_expected_data(
            serializer,
            serializer.Meta.model,
            self.object,
        )
        self.assertEqual(response.data, expected_data)


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
