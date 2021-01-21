# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.api.serializers.rubric import RubricSerializer
from huxley.core.models import Committee


class CommitteeSerializer(serializers.ModelSerializer):
    rubric = RubricSerializer(read_only=True)

    class Meta:
        model = Committee
        fields = ('id',
                  'name',
                  'full_name',
                  'delegation_size',
                  'rubric',
                  'special',
                  'zoom_link', )
