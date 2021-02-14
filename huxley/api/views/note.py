# Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).
import datetime

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from huxley.api.mixins import ListUpdateModelMixin
from huxley.api import permissions
from huxley.api.serializers import NoteSerializer
from huxley.core.models import Note


class NoteList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (permissions.NotePermission, )
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.all()
        query_params = self.request.GET
        sender_id = query_params.get('sender_id', None)
        timestamp = query_params.get('timestamp', None)
        committee_id = query_params.get('committee_id', None)

        if not timestamp:
            return Note.objects.none()

        # Divide by 1000 because fromtimestamp takes in value in seconds
        timestamp_date = datetime.datetime.fromtimestamp(
            int(timestamp) / 1000.0)

        if committee_id and timestamp:
            queryset = queryset.filter(
                sender__committee_id=committee_id).filter(
                    timestamp__gte=timestamp_date) | queryset.filter(
                        recipient__committee_id=committee_id).filter(
                            timestamp__gte=timestamp_date)

        if sender_id and timestamp:
            queryset = queryset.filter(sender_id=sender_id).filter(
                timestamp__gte=timestamp_date) | queryset.filter(
                    recipient_id=sender_id).filter(
                        timestamp__gte=timestamp_date)

        return queryset


class NoteDetail(generics.CreateAPIView, generics.RetrieveAPIView):
    authentication_classes = (SessionAuthentication, )
    queryset = Note.objects.all()
    permission_classes = (permissions.NotePermission, )
    serializer_class = NoteSerializer
