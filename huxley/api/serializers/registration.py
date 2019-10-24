# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.core.models import Committee, Registration
from django.core.mail import send_mail


class RegistrationSerializer(serializers.ModelSerializer):
    delegate_fees_owed = serializers.FloatField(read_only=True)
    delegate_fees_paid = serializers.FloatField(read_only=True)
    assignments_finalized = serializers.BooleanField(required=False)
    country_preferences = serializers.ListField(
        child=serializers.IntegerField(required=False),
        source='country_preference_ids',
        required=False)
    committee_preferences = serializers.PrimaryKeyRelatedField(
        allow_empty=True,
        many=True,
        queryset=Committee.objects.all(),
        required=False)

    class Meta:
        model = Registration
        fields = ('id',
                  'school',
                  'conference',
                  'registered_at',
                  'is_waitlisted',
                  'num_beginner_delegates',
                  'num_intermediate_delegates',
                  'num_advanced_delegates',
                  'num_spanish_speaking_delegates',
                  'num_chinese_speaking_delegates',
                  'waivers_completed',
                  'country_preferences',
                  'committee_preferences',
                  'registration_comments',
                  'delegate_fees_owed',
                  'delegate_fees_paid',
                  'registration_fee_paid',
                  'assignments_finalized',
                  'modified_at', )
        extra_kwargs = {
            'committee_preferences': {'required': False},
            'country_preferences': {'required': False},
            'num_beginner_delegates': {'required': False},
            'num_intermediate_delegates': {'required': False},
            'num_advanced_delegates': {'required': False},
            'num_spanish_speaking_delegates': {'required': False},
            'num_chinese_speaking_delegates': {'required': False},
            'registration_comments': {'required': False}
        }

    def update(self, instance, validated_data):
        if ('assignments_finalized' in validated_data):
            finalized = validated_data['assignments_finalized']
            if bool(finalized) and finalized != 'False':
                    send_mail('{0} has finalized its assignments'.format(instance.school),
                      'New information for {0}: \n\n'.format(instance.school) \
                          + 'Assignments have been finalized!',
                      'tech@bmun.org',
                      ['info@bmun.org', 'admin@bmun.org'], fail_silently=False)

        return super(RegistrationSerializer, self).update(instance, validated_data)

    def validate(self, data):
        invalid_fields = {}

        num_beginner_delegates = data.get('num_beginner_delegates')
        num_intermediate_delegates = data.get('num_intermediate_delegates')
        num_advanced_delegates = data.get('num_advanced_delegates')
        num_spanish_speaking_delegates = data.get(
            'num_spanish_speaking_delegates')
        num_chinese_speaking_delegates = data.get(
            'num_chinese_speaking_delegates')

        total_delegates = sum(
            (num_beginner_delegates or 0, num_intermediate_delegates or 0,
             num_advanced_delegates or 0))

        if num_beginner_delegates and num_beginner_delegates >= 200:
            invalid_fields[
                'num_beginner_delegates'] = 'Cannot register that many delegates.'
        if num_intermediate_delegates and num_intermediate_delegates >= 200:
            invalid_fields[
                'num_intermediate_delegates'] = 'Cannot register that many delegates.'
        if num_advanced_delegates and num_advanced_delegates >= 200:
            invalid_fields[
                'num_advanced_delegates'] = 'Cannot register that many delegates.'

        if num_advanced_delegates and num_spanish_speaking_delegates > total_delegates:
            invalid_fields[
                'num_spanish_speaking_delegates'] = 'Cannot exceed total number of delegates.'
        if num_chinese_speaking_delegates and num_chinese_speaking_delegates > total_delegates:
            invalid_fields[
                'num_chinese_speaking_delegates'] = 'Cannot exceed total number of delegates.'

        if invalid_fields:
            raise serializers.ValidationError(invalid_fields)

        return data
