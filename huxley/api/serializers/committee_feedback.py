# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.api import validators
from huxley.core.models import CommitteeFeedback


class CommitteeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitteeFeedback
        fields = ('id',
                  'committee',
                  'comment',
                  'rating',
                  'chair_1_name',
                  'chair_2_name',
                  'chair_3_name',
                  'chair_4_name',
                  'chair_5_name',
                  'chair_6_name',
                  'chair_7_name',
                  'chair_8_name',
                  'chair_9_name',
                  'chair_10_name',
                  'chair_1_comment',
                  'chair_2_comment',
                  'chair_3_comment',
                  'chair_4_comment',
                  'chair_5_comment',
                  'chair_6_comment',
                  'chair_7_comment',
                  'chair_8_comment',
                  'chair_9_comment',
                  'chair_10_comment',
                  'chair_1_rating',
                  'chair_2_rating',
                  'chair_3_rating',
                  'chair_4_rating',
                  'chair_5_rating',
                  'chair_6_rating',
                  'chair_7_rating',
                  'chair_8_rating',
                  'chair_9_rating',
                  'chair_10_rating', )
