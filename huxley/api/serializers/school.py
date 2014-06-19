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
                  'primary_phone', 'primary_gender', 'primary_type',
                  'secondary_name', 'secondary_email', 'secondary_gender',
                  'secondary_phone','secondary_type', 'program_type',
                  'times_attended','delegation_size','international', 'waitlist')

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
            'State contains invalid characters.')

        return attrs

    def validate_school_country(self, attrs, source):
        school_country = attrs[source]

        if attrs['school_location'] == School.LOCATION_INTERNATIONAL and not school_country:
            raise forms.ValidationError('International schools must provide a country.')

        validate_alphabetical(school_country,
            'Country contains invalid characters.')

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

        validators.validate_alphanumerical(school_address,
            'School address contains invalid characters.')

        return attrs

    def validate_school_city(self, attrs, source):
        school_city = attrs[source]

        validators.validate_alphabetical(school_city,
            'School city contains invalid characters.')

        return attrs

    def validate_school_zip(self, attrs, source):
        school_zip = attrs[source]

        validators.validate_numerical(school_zip,
            'School zip contains invalid characters.')

        return attrs

    def validate_times_attended(self, attrs, source):
        times_attended = attrs[source]

        print(type(times_attended))

        validators.validate_numerical(times_attended,
            'Times attended contains invalid characters.')

        return attrs

    def validate_delegation_size(self, attrs, source):
        delegation_size = attrs[source]

        validators.validate_numerical(delegation_size,
            'Delegation size contains invalid characters.')

        return attrs

    def validate_primary_name(self, attrs, source):
        primary_name = attrs[source]

        validators.validate_alphabetical(primary_name,
            'Primary name contains invalid characters.')

        return attrs

    def validate_primary_email(self, attrs, source):
        primary_email = attrs[source]

        validators.validate_email(primary_email,
            'Primary email contains invalid characters.')

        return attrs

    def validate_primary_phone(self, attrs, source):
        primary_phone = attrs[source]

        validators.validate_numerical(primary_phone,
            'Primary phone contains invalid characters.')

        return attrs

    def validate_secondary_name(self, attrs, source):
        secondary_name = attrs.get(source, '')

        if(secondary_name != ''):
            validators.validate_alphabetical(secondary_name,
                'Secondary name contains invalid characters.')

        return attrs

    def validate_secondary_email(self, attrs, source):
        secondary_email = attrs.get(source, '')

        if(secondary_email != ''):
            validators.validate_email(secondary_email,
                'Secondary email contains invalid characters.')

        return attrs

    def validate_secondary_phone(self, attrs, source):
        secondary_phone = attrs.get(source, '')

        if(secondary_phone != ''):
            validators.validate_numerical(secondary_phone,
                'Secondary phone contains invalid characters.')

        return attrs
