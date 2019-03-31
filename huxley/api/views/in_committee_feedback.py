# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core import validators

from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication

from huxley.api import permissions
from huxley.api.serializers import InCommitteeFeedbackSerializer
from huxley.core.models import InCommitteeFeedback


class InCommitteeFeedbackList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (permissions.InCommitteeFeedbackListPermission, )
    serializer_class = InCommitteeFeedbackSerializer

    def get_queryset(self):
        queryset = InCommitteeFeedback.objects.all()

        assignment_id = self.request.query_params.get('assignment_id', None)
        if assignment_id:
            queryset = queryset.filter(assignment_id=assignment_id)

        return queryset


class InCommitteeFeedbackDetail(generics.CreateAPIView,
                              generics.RetrieveAPIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (permissions.InCommitteeFeedbackDetailPermission, )
    serializer_class = InCommitteeFeedbackSerializer
    queryset = InCommitteeFeedback.objects.all()
