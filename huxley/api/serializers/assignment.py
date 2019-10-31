# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.api.serializers.committee import CommitteeSerializer
from huxley.api.serializers.country import CountrySerializer
from huxley.api.serializers.position_paper import PositionPaperSerializer
from huxley.core.models import Assignment, Registration
from django.core.mail import send_mail


class AssignmentSerializer(serializers.ModelSerializer):
    paper = PositionPaperSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ('id', 'committee', 'country', 'paper', 'registration',
                  'rejected')

    def update(self, instance, validated_data):
        print(validated_data)
        if ('rejected' in validated_data):
            rejected = validated_data['rejected']
            print(rejected)
            if bool(rejected):
                send_mail('{0} has deleted an assignment'.format(instance.registration.school),
                    'New information for {0}: \n\n'.format(instance.registration.school) \
                        + 'Assignment {0}: {1} has been deleted.'.format(instance.committee, instance.country),
                    'tech@bmun.org',
                    ['info@bmun.org', 'admin@bmun.org'], fail_silently=False)

        return super(AssignmentSerializer, self).update(instance, validated_data)



class AssignmentNestedSerializer(serializers.ModelSerializer):
    committee = CommitteeSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    paper = PositionPaperSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ('id', 'committee', 'country', 'paper', 'registration',
                  'rejected')
