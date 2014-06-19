# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.core.models import School


class SchoolSerializer(serializers.ModelSerializer):
    registered = serializers.DateTimeField(format='iso-8601', required=False)

    class Meta:
        model = School
        # TODO: country/committee preferences
        fields = (
            'id',
            'registered',
            'name',
            'address',
            'city',
            'state',
            'zip_code',
            'country',
            'primary_name',
            'primary_gender',
            'primary_email',
            'primary_phone',
            'primary_type',
            'secondary_name',
            'secondary_gender',
            'secondary_email',
            'secondary_phone',
            'secondary_type',
            'program_type',
            'times_attended',
            'delegation_size',
            'international',
            'waitlist',
            'registration_comments',
        )
