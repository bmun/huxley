# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.core.models import Note

class TimestampField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return value.timestamp.timestamp()

class NoteSerializer(serializers.ModelSerializer):
    timestamp = TimestampField(source='*')
    class Meta:
        model = Note
        fields = ('id', 'is_chair', 'sender', 'recipient', 'msg', 'timestamp')
