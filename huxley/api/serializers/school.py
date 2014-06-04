# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.core.models import School


class SchoolSerializer(serializers.ModelSerializer):
    registered = serializers.DateTimeField(format='iso-8601', required=False)

    class Meta:
        model = School
        # TODO: country/committee preferences
        fields = ('id', 'registered', 'name', 'address', 'city', 'state',
                  'zip_code', 'country', 'primary_name', 'primary_email',
                  'primary_phone', 'secondary_name', 'secondary_email',
                  'secondary_phone', 'program_type', 'times_attended',
                  'min_delegation_size', 'max_delegation_size',
                  'international', 'waitlist')
