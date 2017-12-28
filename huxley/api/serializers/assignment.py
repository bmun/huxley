# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.api.serializers.committee import CommitteeSerializer
from huxley.api.serializers.country import CountrySerializer
from huxley.api.serializers.position_paper import PositionPaperSerializer
from huxley.core.models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    paper = PositionPaperSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ('id', 'committee', 'country', 'paper', 'registration', 'rejected')


class AssignmentNestedSerializer(serializers.ModelSerializer):
    committee = CommitteeSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    paper = PositionPaperSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ('id', 'committee', 'country', 'paper', 'registration', 'rejected')
