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

    def validate_name(self, attrs, source):
        school_name = attrs[source]

        if School.objects.filter(name=school_name).exists():
            raise serializers.ValidationError(
                'A school with the name "%s" has already been registered.'
                % (school_name))

            validators.alphanumeric(school_name, 'name')

        return attrs

    def validate_state(self, attrs, source):
        school_state = attrs[source]

        validators.alphabetical(school_state, 'state')

        return attrs

    def validate_country(self, attrs, source):
        school_country = attrs[source]

        validators.alphabetical(school_country, 'country')

        return attrs

    def validate_primary_phone(self, attrs, source):
        international = attrs['international']
        number = attrs[source]

        if international == School.LOCATION_INTERNATIONAL:
            if(bool(re.match("^[0-9\-x\s\+\(\)]+$", number))):
                return attrs
            else:
               raise serializers.ValidationError('primary_phone contains invalid characters.')
        else:
            if(bool(re.match("^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$", number))):
                return attrs
            else:
                raise serializers.ValidationError('primary_phone contains invalid characters.')

    def validate_address(self, attrs, source):
        school_address = attrs[source]

        validators.alphanumeric(school_address, 'address')

        return attrs

    def validate_city(self, attrs, source):
        school_city = attrs[source]

        validators.alphabetical(school_city, 'city')

        return attrs

    def validate_zip(self, attrs, source):
        school_zip = attrs[source]

        validators.numerical(school_zip, 'zip')

        return attrs

    def validate_primary_name(self, attrs, source):
        primary_name = attrs[source]

        validators.alphabetical(primary_name, 'primary_name')

        return attrs

    def validate_primary_email(self, attrs, source):
        primary_email = attrs[source]

        validators.email(primary_email, 'primary_email')

        return attrs

    def validate_secondary_name(self, attrs, source):
        secondary_name = attrs.get(source, '')

        if(secondary_name != ''):
            validators.alphabetical(secondary_name, 'secondary_name')

        return attrs

    def validate_secondary_email(self, attrs, source):
        secondary_email = attrs.get(source, '')

        if(secondary_email != ''):
            validators.email(secondary_email, 'secondary_email')

        return attrs

    def validate_secondary_phone(self, attrs, source):
        secondary_phone = attrs.get(source, '')

        if(secondary_phone != ''):
            validators.numerical(secondary_phone, 'secondary_phone')

        return attrs
