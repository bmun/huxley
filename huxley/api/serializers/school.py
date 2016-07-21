# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).
from rest_framework import serializers

from huxley.api import validators
from huxley.core.models import School, Committee


class SchoolSerializer(serializers.ModelSerializer):
    fees_owed = serializers.FloatField(read_only=True)
    fees_paid = serializers.FloatField(read_only=True)
    assignments_finalized = serializers.BooleanField(required=False)
    countrypreferences = serializers.ListField(child=serializers.IntegerField(required=False), source='country_preference_ids')
    committeepreferences = serializers.PrimaryKeyRelatedField(allow_empty=True, many=True, queryset=Committee.objects.all(), required=False)

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
            'waivers_completed',
            'countrypreferences',
            'committeepreferences',
            'registration_comments',
            'fees_owed',
            'fees_paid',
            'assignments_finalized',
            'modified_at',
        )
        extra_kwargs = {
        'committeepreferences': {'required': False},
        'countrypreferences': {'required': False},
        'secondary_name': {'required': False},
        'secondary_gender': {'required': False},
        'secondary_email': {'required': False},
        'secondary_phone': {'required': False},
        'secondary_type': {'required': False},
        'program_type': {'required': False},
        'times_attended': {'required': False},
        'beginner_delegates': {'required': False},
        'intermediate_delegates': {'required': False},
        'advanced_delegates': {'required': False},
        'spanish_speaking_delegates': {'required': False},
        'chinese_speaking_delegates': {'required': False},
        'countrypreferences': {'required': False},
        'committeepreferences': {'required': False},
        'registration_comments': {'required': False}
        }


    def validate(self, data):
        invalid_fields = {}
        international = data.get('international')
        primary_phone = data.get('primary_phone')
        secondary_phone = data.get('secondary_phone')
        beginner_delegates = data.get('beginner_delegates')
        intermediate_delegates = data.get('intermediate_delegates')
        advanced_delegates = data.get('advanced_delegates')
        spanish_speaking_delegates = data.get('spanish_speaking_delegates')
        chinese_speaking_delegates = data.get('chinese_speaking_delegates')

        total_delegates = sum((
            beginner_delegates or 0,
            intermediate_delegates or 0,
            advanced_delegates or 0))

        def validate_phone(phone, international):
            if international:
                validators.phone_international(phone)
            else:
                validators.phone_domestic(phone)

        if primary_phone:
            try:
                validate_phone(primary_phone, international)
            except serializers.ValidationError:
                invalid_fields['primary_phone'] = 'This is an invalid phone number.'
        if secondary_phone:
            try:
                validate_phone(secondary_phone, international)
            except serializers.ValidationError:
                invalid_fields['secondary_phone'] = 'This is an invalid phone number.'

        if spanish_speaking_delegates > total_delegates:
            invalid_fields['spanish_speaking_delegates'] = 'Cannot exceed total number of delegates.'
        if chinese_speaking_delegates > total_delegates:
            invalid_fields['chinese_speaking_delegates'] = 'Cannot exceed total number of delegates.'

        if invalid_fields:
            raise serializers.ValidationError(invalid_fields)

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

    def validate_zip_code(self, value):
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
