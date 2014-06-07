# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import re

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

    def validate_school_name(self, attrs, source):
        school_name = attrs[source]

        if School.objects.filter(name=school_name).exists():
            raise forms.ValidationError(
                'A school with the name "%s" has already been registered.'
                % (school_name))

        if re.match("^[A-Za-z0-9\s]+$", school_name) is None:
            raise ValidationError(
                'A school name may only contain alphanumeric characters.')

        return attrs

    def validate_school_state(self, attrs, source):
        school_state = attrs[source]

        if attrs['school_location'] == School.LOCATION_USA and not school_state:
            raise forms.ValidationError(
                'You must provide a state for a school in the United States.')

        if re.match("^[A-Za-z\s]+$", school_state) is None:
            raise ValidationError(
                'States may only contain alphabetical characters.')

        return attrs

    def validate_school_country(self, attrs, source):
        school_country = attrs[source]

        if attrs['school_location'] == School.LOCATION_INTERNATIONAL and not school_country:
            raise forms.ValidationError('International schools must provide a country.')

        if re.match("^[A-Za-z\s]+$", school_state) is None:
            raise ValidationError(
                'Countries may only contain alphabetical characters.')

        return attrs

    def validate_phone(self, attrs, source):

