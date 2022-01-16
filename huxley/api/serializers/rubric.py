# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.core.models import Rubric


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'grade_category_1', 'grade_category_2',
                  'grade_category_3', 'grade_category_4', 'grade_category_5',
                  'grade_value_1', 'grade_value_2', 'grade_value_3',
                  'grade_value_4', 'grade_value_5', 'use_topic_2',
                  'grade_t2_category_1', 'grade_t2_category_2',
                  'grade_t2_category_3', 'grade_t2_category_4',
                  'grade_t2_category_5', 'grade_t2_value_1',
                  'grade_t2_value_2', 'grade_t2_value_3', 'grade_t2_value_4',
                  'grade_t2_value_5', 'topic_one', 'topic_two')
