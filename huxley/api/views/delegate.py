# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from huxley.api.mixins import ListUpdateModelMixin
from huxley.api.permissions import IsSchoolDelegateAdvisorOrSuperuser, IsPostOrSuperuserOnly, IsChairOrSuperuser
from huxley.api.serializers import DelegateSerializer
from huxley.core.models import Delegate


class DelegateList(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Delegate.objects.all()
    permission_classes = (IsPostOrSuperuserOnly,)
    serializer_class = DelegateSerializer


class DelegateDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Delegate.objects.all()
    permission_classes = (IsSchoolDelegateAdvisorOrSuperuser,)
    serializer_class = DelegateSerializer

class DelegateCommitteeDetail(generics.ListAPIView, ListUpdateModelMixin):
    authentication_classes = (SessionAuthentication,)
    queryset = Delegate.objects.all()
    serializer_class = DelegateSerializer
    permission_classes = (IsChairOrSuperuser,)

    def get_queryset(self):
        '''Filter schools by the given pk param.'''
        committee_id = self.kwargs.get('pk', None)
        if not committee_id:
            raise Http404
        return Delegate.objects.filter(assignment__committee_id=committee_id)

    def patch(self, request, *args, **kwargs):
        return self.list_update(request, partial=True, *args, **kwargs)
