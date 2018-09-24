# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.core.models import SecretariatMember


class SecretariatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretariatMember
        fields = ('id',
                  'name',
                  'committee',
                  'is_head_chair', )
