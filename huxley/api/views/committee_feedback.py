# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api import permissions
from huxley.api.serializers import CommitteeFeedbackSerializer
from huxley.core.models import CommitteeFeedback

class CommitteeFeedbackList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.CommitteeFeedbackListPermission,)
    serializer_class = CommitteeFeedbackSerializer

    def get_queryset(self):
        queryset = CommitteeFeedback.objects.all()
        user = self.request.GET
        
        committee_id = query_params.get('committee_id',None)
        if committee_id:
            queryset = queryset.filter(committee__id=committee_id)

        return queryset

class CommitteeFeedbackDetail(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.CommitteeFeedbackDetailPermission,)
    serializer_class = CommitteeFeedbackSerializer

