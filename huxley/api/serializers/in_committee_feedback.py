# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.api import validators
from huxley.core.models import InCommitteeFeedback


class InCommitteeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InCommitteeFeedback
        fields = ('id',
                  'feedback',
                  'assignment',
                  'speech',
                  'score', )
