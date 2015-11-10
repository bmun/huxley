# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).
from rest_framework import serializers

from huxley.api import validators
from huxley.api.serializers.fields import DecimalField
from huxley.core.models import School


class SchoolSerializer(serializers.ModelSerializer):
    registered = serializers.DateTimeField(format='iso-8601', required=False)
    fees_owed = DecimalField(max_digits=10, decimal_places=2, read_only=True, coerce_to_string=False)
    fees_paid = DecimalField(max_digits=10, decimal_places=2, read_only=True, coerce_to_string=False)
    assignments_finalized = serializers.BooleanField(required=False)
    country_preferences = serializers.ListField(serializers.IntegerField())

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

    def validate(self, data):
        international = data.get('international')
        primary_phone = data.get('primary_phone')
        secondary_phone = data.get('secondary_phone')

        if primary_phone:
            if international:
                validators.phone_international(primary_phone)
            else:
                validators.phone_domestic(primary_phone)
        if secondary_phone:
            if international:
                validators.phone_international(secondary_phone)
            else:
                validators.phone_domestic(secondary_phone)

        return data

    def validate_name(self, value):
        school_name = value

        if School.objects.filter(name=school_name).exists():
            raise serializers.ValidationError(
                'A school with the name "%s" has already been registered.'
                % school_name)

        validators.name(school_name)

        return value

    def validate_state(self, value):
        school_state = value

        validators.name(school_state)

        return value

    def validate_country(self, value):
        school_country = value

        validators.name(school_country)

        return value

    def validate_address(self, value):
        school_address = value

        validators.address(school_address)

        return value

    def validate_city(self, value):
        school_city = value

        validators.name(school_city)

        return value

    def validate_zip(self, value):
        school_zip = value

        validators.numeric(school_zip)

        return value

    def validate_primary_name(self, value):
        primary_name = value

        validators.name(primary_name)

        return value

    def validate_primary_email(self, value):
        primary_email = value

        validators.email(primary_email)

        return value

    def validate_secondary_name(self, value):
        secondary_name = value

        if secondary_name:
            validators.name(secondary_name)

        return value

    def validate_secondary_email(self, value):
        secondary_email = value

        if secondary_email:
            validators.email(secondary_email)

        return value
