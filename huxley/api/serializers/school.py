# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import re

from rest_framework import serializers

from huxley.core.models import School
from huxley.api import validators


class SchoolSerializer(serializers.ModelSerializer):
    registered = serializers.DateTimeField(format='iso-8601', required=False)

    class Meta:
        model = School
        # TODO: country/committee preferences
        fields = ('id', 'registered', 'name', 'address', 'city', 'state',
                  'zip_code', 'country', 'primary_name', 'primary_email',
                  'primary_phone', 'secondary_name', 'secondary_email',
                  'secondary_phone', 'program_type', 'times_attended',
                  'delegation_size',
                  'international', 'waitlist')

    def validate_school_name(self, attrs, source):
        school_name = attrs[source]

        if School.objects.filter(name=school_name).exists():
            raise forms.ValidationError(
                'A school with the name "%s" has already been registered.'
                % (school_name))

            validate_alphanumerical(school_name,
                'A school name may only contain alphanumeric characters.')

        return attrs

    def validate_school_state(self, attrs, source):
        school_state = attrs[source]

        if attrs['school_location'] == School.LOCATION_USA and not school_state:
            raise forms.ValidationError(
                'You must provide a state for a school in the United States.')

        validate_alphabetical(school_state,
            'States may only contain alphabetical characters.')

        return attrs

    def validate_school_country(self, attrs, source):
        school_country = attrs[source]

        if attrs['school_location'] == School.LOCATION_INTERNATIONAL and not school_country:
            raise forms.ValidationError('International schools must provide a country.')

        validate_alphabetical(school_country,
            'Countries may only contain alphabetical characters.')

        return attrs

    def validate_phone(self, attrs, source):
        international = attrs['international']
        number = attrs[source]

        if international == School.LOCATION_INTERNATIONAL:
            return bool(re.match("^[0-9\-x\s\+\(\)]+$", number))
        else:
            return bool(re.match("^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$", number))

    def validate_school_address(self, attrs, source):
        school_address = attrs[source]

        validate_alphanumerical(school_address,
            'School address should be alphanumeric.')

        return attrs

    def validate_school_city(self, attrs, source):
        school_city = attrs[source]

        validate_alphabetical(school_city,
            'School city should be validate_alphabetical.')

        return attrs

    def validate_school_zip(self, attrs, source):
        school_zip = attrs[source]

        validate_numerical(school_zip,
            'School zip should be numerical.')

        return attrs

    def validate_times_attended(self, attrs, source):
        if(attrs != None):
            times_attended = attrs[source]

            validate_numerical(times_attended,
                'Times attended must be numerical')

            return attrs

        else:
            pass


    def validate_delegation_size(self, attrs, source):
        if(attrs != None):
            delegation_size = attrs[source]

            validate_numerical(delegation_size,
                'Delegation size must be numerical.')

            return attrs

        else:
            pass

    def validate_primary_name(self, attrs, source):
        primary_name = attrs[source]

        validators.validate_alphabetical(primary_name,
            'Primary name must be alphanumeric.')

        return attrs

    '''def validate_primary_email(self, attrs, source):
        if(attrs != None):
            primary_email = attrs[source]

            validators.validate_email(primary_email,
                'Email can only contain ')

            return attrs

        else:
            pass'''

    def validate_primary_phone(self, attrs, source):
        pass

    def validate_secondary_name(self, attrs, source):
        pass

    def validate_secondary_email(self, attrs, source):
        pass

    def validate_secondary_phone(self, attrs, source):
        pass
