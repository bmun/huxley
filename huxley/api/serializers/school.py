# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from drf_compound_fields.fields import ListField
from rest_framework import serializers

from huxley.api import validators
from huxley.api.serializers.fields import DecimalField
from huxley.core.models import School


class SchoolSerializer(serializers.ModelSerializer):
    registered = serializers.DateTimeField(format='iso-8601', required=False)
    fees_owed = DecimalField(read_only=True)
    fees_paid = DecimalField(read_only=True)
    assignments_finalized = serializers.BooleanField()
    country_preferences = ListField(
        serializers.IntegerField(),
        source='country_preference_ids')

    class Meta:
        model = School
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
            'international',
            'waitlist',
            'beginner_delegates',
            'intermediate_delegates',
            'advanced_delegates',
            'spanish_speaking_delegates',
            'chinese_speaking_delegates',
            'country_preferences',
            'committeepreferences',
            'registration_comments',
            'fees_owed',
            'fees_paid',
            'assignments_finalized',
        )

    def validate_name(self, attrs, source):
        school_name = attrs[source]

        if School.objects.filter(name=school_name).exists():
            raise serializers.ValidationError(
                'A school with the name "%s" has already been registered.'
                % school_name)

        validators.name(school_name)

        return attrs

    def validate_state(self, attrs, source):
        school_state = attrs[source]

        validators.name(school_state)

        return attrs

    def validate_country(self, attrs, source):
        school_country = attrs[source]

        validators.name(school_country)

        return attrs

    def validate_primary_phone(self, attrs, source):
        international = attrs['international']
        number = attrs[source]

        if international:
            validators.phone_international(number)
        else:
            validators.phone_domestic(number)

        return attrs

    def validate_address(self, attrs, source):
        school_address = attrs[source]

        validators.address(school_address)

        return attrs

    def validate_city(self, attrs, source):
        school_city = attrs[source]

        validators.name(school_city)

        return attrs

    def validate_zip(self, attrs, source):
        school_zip = attrs[source]

        validators.numeric(school_zip)

        return attrs

    def validate_primary_name(self, attrs, source):
        primary_name = attrs[source]

        validators.name(primary_name)

        return attrs

    def validate_primary_email(self, attrs, source):
        primary_email = attrs[source]

        validators.email(primary_email)

        return attrs

    def validate_secondary_name(self, attrs, source):
        secondary_name = attrs.get(source)

        if secondary_name:
            validators.name(secondary_name)

        return attrs

    def validate_secondary_email(self, attrs, source):
        secondary_email = attrs.get(source)

        if secondary_email:
            validators.email(secondary_email)

        return attrs

    def validate_secondary_phone(self, attrs, source):
        number = attrs.get(source)
        international = attrs['international']

        if number:
            if international:
                validators.phone_international(number)
            else:
                validators.phone_domestic(number)

        return attrs
