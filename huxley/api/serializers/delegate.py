# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.api.serializers.assignment import AssignmentNestedSerializer
from huxley.api.serializers.school import SchoolSerializer
from huxley.core.models import Delegate


class DelegateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delegate
        fields = (
            'id', 
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
        )

class DelegateNestedSerializer(serializers.ModelSerializer):
    assignment = AssignmentNestedSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = Delegate
        fields = (
            'id', 
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
        )
