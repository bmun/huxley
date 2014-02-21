# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from rest_framework import serializers

from huxley.accounts.models import HuxleyUser
from huxley.core.models import Committee

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuxleyUser
        fields = ('id', 'first_name', 'last_name', 'user_type', 'school',
                  'committee',)

class CommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields = ('id', 'name', 'full_name', 'delegation_size', 'special',)
