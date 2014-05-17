# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import re

from rest_framework.serializers import ModelSerializer, ValidationError

from huxley.accounts.models import HuxleyUser
from huxley.api.serializers.committee import CommitteeSerializer
from huxley.api.serializers.school import SchoolSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = HuxleyUser
        fields = ('id', 'username', 'first_name', 'last_name', 'user_type',
                  'school', 'committee',)
        read_only_fields = tuple(fields)


class CreateUserSerializer(ModelSerializer):
    school = SchoolSerializer(required=False) # TODO: CreateSchoolSerializer

    class Meta:
        model = HuxleyUser
        fields = ('id', 'username', 'password', 'first_name', 'last_name',
                  'user_type', 'school',)
        read_only_fields = ('user_type',)
        write_only_fields = ('password',)

    def restore_object(self, attrs, instance=None):
        original_attrs = attrs.copy()
        if 'password' in attrs:
            del attrs['password']

        user = super(CreateUserSerializer, self).restore_object(attrs, instance)
        if 'password' in original_attrs:
            user.set_password(original_attrs['password'])
        if 'school' in original_attrs:
            user.user_type = HuxleyUser.TYPE_ADVISOR

        return user

    def validate_username(self, attrs, source):
        username = attrs[source]

        if re.match("^[A-Za-z0-9\_\-]+$", username) is None:
            raise ValidationError('Usernames may contain alphanumerics, '
                                  'underscores, and/or hyphens only.')

        if HuxleyUser.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')

        return attrs

    def validate_password(self, attrs, source):
        password = attrs[source]

        match = re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", password)
        if match is None:
            raise ValidationError('Password contains invalid characters.')

        return attrs
