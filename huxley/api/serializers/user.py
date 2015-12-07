# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import re

from rest_framework.serializers import ModelSerializer, ValidationError, CharField

from huxley.accounts.models import User, School
from huxley.api import validators
from huxley.api.serializers.school import SchoolSerializer


class UserSerializer(ModelSerializer):
    school = SchoolSerializer(required=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'user_type',
                  'school', 'committee',)
        read_only_fields = ('id', 'username', 'first_name', 'last_name',
                            'user_type', 'committee',)


class CreateUserSerializer(ModelSerializer):
    school = SchoolSerializer(required=False) # TODO: CreateSchoolSerializer

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name',
                  'user_type', 'school', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
            'user_type': {'read_only': True}
        }

    def create(self, validated_data):
        original_validated_data = validated_data.copy()

        if 'password' in validated_data:
            del validated_data['password']

        if validated_data.get('school'):
            school_data = validated_data.pop('school')
            committeepreferences = school_data.pop('committeepreferences')

            school = School.objects.create(**school_data)
            school.save()

            for pref in committeepreferences:
                school.committeepreferences.add(pref)
            school.save()

            user = User.objects.create(school=school, **validated_data)
        else:
            user = User.objects.create(**validated_data)

        if 'password' in original_validated_data:
            user.set_password(original_validated_data['password'])
            user.save()
        if 'school' in original_validated_data:
            user.user_type = User.TYPE_ADVISOR
            user.save()

        return user

    def validate_username(self, value):
        username = value

        if re.match("^[A-Za-z0-9\_\-]+$", username) is None:
            raise ValidationError('Usernames may contain alphanumerics, '
                                  'underscores, and/or hyphens only.')

        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')

        if len(username) < 5:
            raise ValidationError('Username must be at least 5 characters.')

        return value

    def validate_password(self, value):
        password = value

        match = re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", password)
        if match is None:
            raise ValidationError('Password contains invalid characters.')

        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters.')

        return value

    def validate_first_name(self, value):
        first_name = value
        validators.nonempty(first_name)
        return value

    def validate_last_name(self, value):
        last_name = value
        validators.nonempty(last_name)
        return value

