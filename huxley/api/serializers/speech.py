# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers
from huxley.api.serializers.assignment import AssignmentSerializer
from huxley.core.models import Speech

class SpeechSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)

    class Meta:
        model = Speech
        fields = ('assignment',
                'speechtype',)
