# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
import rest_framework

from huxley.api.mixins import ListUpdateModelMixin
from huxley.api.permissions import IsSchoolDelegateAdvisorOrSuperuser, IsPostOrSuperuserOnly, IsChairOrSuperuser
from huxley.api.serializers import DelegateSerializer
from huxley.core.models import Delegate


class DelegateList(generics.ListAPIView, ListUpdateModelMixin):
    authentication_classes = (SessionAuthentication,)
    permission_classes = [rest_framework.permissions.AllowAny,]
    serializer_class = DelegateSerializer

    def get_queryset(self):
        '''Filter delegates by the given committee_id param.'''
        committee_id = self.request.query_params.get('committee_id', None)
        if committee_id:
            return Delegate.objects.filter(assignment__committee_id=committee_id)
        return Delegate.objects.all()

    def patch(self, request, *args, **kwargs):
        return self.list_update(request, partial=True, *args, **kwargs)


class DelegateDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Delegate.objects.all()
    permission_classes = (IsSchoolDelegateAdvisorOrSuperuser,)
    serializer_class = DelegateSerializer
