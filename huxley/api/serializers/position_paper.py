# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.core.models import PositionPaper


class PositionPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionPaper
        fields = ('id', 'file', 'graded', 'score_1', 'score_2', 'score_3',
                  'score_4', 'score_5', 'submission_date')
