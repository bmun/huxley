# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core import validators

from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication

from huxley.api import permissions
from huxley.api.serializers import CommitteeFeedbackSerializer
from huxley.core.models import CommitteeFeedback, Delegate


class CommitteeFeedbackList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (permissions.CommitteeFeedbackListPermission, )
    serializer_class = CommitteeFeedbackSerializer

    def get_queryset(self):
        queryset = CommitteeFeedback.objects.all()

        committee_id = self.request.query_params.get('committee_id', None)
        if committee_id:
            queryset = queryset.filter(committee__id=committee_id)

        return queryset


class CommitteeFeedbackDetail(generics.CreateAPIView,
                              generics.RetrieveAPIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (permissions.CommitteeFeedbackDetailPermission, )
    serializer_class = CommitteeFeedbackSerializer
    queryset = CommitteeFeedback.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            self.request.user.delegate.committee_feedback_submitted = True
            self.request.user.delegate.save()
        super(CommitteeFeedbackDetail, self).perform_create(serializer)
