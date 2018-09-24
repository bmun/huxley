# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from huxley.accounts.models import User
from huxley.api.serializers.assignment import AssignmentNestedSerializer
from huxley.api.serializers.school import SchoolSerializer
from huxley.core.models import Assignment, Delegate


class DelegateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delegate
        fields = ('id',
                  'assignment',
                  'name',
                  'email',
                  'created_at',
                  'summary',
                  'published_summary',
                  'school',
                  'voting',
                  'session_one',
                  'session_two',
                  'session_three',
                  'session_four',
                  'committee_feedback_submitted',
                  'waiver_submitted', )

    def update(self, instance, validated_data):
        if ('assignment' in validated_data and
                validated_data['assignment'] != None and
                not User.objects.filter(delegate__id=instance.id).exists()):

            names = instance.name.split(' ')
            username = names[0] + '_' + str(instance.id)
            password = BaseUserManager().make_random_password(10)
            user = User.objects.create_user(
                username=username,
                password=password,
                delegate=instance,
                user_type=User.TYPE_DELEGATE,
                first_name=names[0],
                last_name=names[-1],
                email=instance.email,
                last_login=datetime.now())

            send_mail('A new account has been created for {0}!'.format(instance.name.encode('utf8')),
                      'Username: {0}\n'.format(username.encode('utf8')) \
                      + 'Password: {0}\n'.format(password) \
                      + 'Please save this information! You will need it for ' \
                      + 'important information and actions. You can access ' \
                      + 'this account at huxley.bmun.org.',
                      'no-reply@bmun.org',
                      [instance.email], fail_silently=False)

        if ('email' in validated_data and
                User.objects.filter(delegate__id=instance.id).exists()):

            user = User.objects.get(delegate__id=instance.id)
            user.email = validated_data['email']
            user.save()

        return super(DelegateSerializer, self).update(instance, validated_data)


class DelegateNestedSerializer(serializers.ModelSerializer):
    assignment = AssignmentNestedSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = Delegate
        fields = ('id',
                  'assignment',
                  'name',
                  'email',
                  'created_at',
                  'summary',
                  'published_summary',
                  'school',
                  'voting',
                  'session_one',
                  'session_two',
                  'session_three',
                  'session_four',
                  'committee_feedback_submitted',
                  'waiver_submitted', )
