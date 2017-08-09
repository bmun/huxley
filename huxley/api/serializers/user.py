# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import re

from rest_framework.serializers import ModelSerializer, ValidationError, CharField

from datetime import datetime

from django.core.mail import send_mail
from django.utils import timezone

from huxley.accounts.models import User, School
from huxley.api import validators
from huxley.api.serializers.school import SchoolSerializer


class UserSerializer(ModelSerializer):
    school = SchoolSerializer(required=False)

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'user_type',
                  'school',
                  'committee',
                  'assignment', )
        read_only_fields = ('id',
                            'username',
                            'user_type',
                            'committee', )

    def update(self, instance, validated_data):
        if 'school' in validated_data:
            school_data = validated_data.pop('school')
            School.objects.filter(id=instance.school.id).update(**school_data)
            send_mail('{0} has updated its information'.format(instance.school),
                      'New information for {0}: \n\n'.format(instance.school) \
                      + 'Advisor: \n' \
                      + '\n'.join(['{0}: {1}'.format(field, validated_data[field]) for field in validated_data]) \
                      + '\n\nSchool: \n' \
                      + '\n'.join(['{0}: {1}'.format(field, school_data[field]) for field in school_data]),
                      'tech@bmun.org',
                      ['info@bmun.org'], fail_silently=False)

        return super(UserSerializer, self).update(instance, validated_data)


class CreateUserSerializer(ModelSerializer):
    school = SchoolSerializer(required=False)

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

            school = School.objects.create(**school_data)
            school.save()

            user = User.objects.create(
                school=school, last_login=datetime.now(), **validated_data)
        else:
            user = User.objects.create(
                last_login=datetime.now(), **validated_data)

        if 'password' in original_validated_data:
            user.set_password(original_validated_data['password'])
            user.save()
        if 'school' in original_validated_data:
            user.user_type = User.TYPE_ADVISOR
            user.save()

        return user

    def validate_username(self, value):
        # Django's User model already handles character and uniqueness
        # validation, so we only worry about length.
        if len(value) < 5:
            raise ValidationError('Username must be at least 5 characters.')

        return value

    def validate_password(self, value):
        password = value

        match = re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$",
                         password)
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
