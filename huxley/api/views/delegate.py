# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from huxley.api.mixins import ListUpdateModelMixin
from huxley.api import permissions
from huxley.api.serializers import DelegateSerializer
from huxley.core.models import Delegate


class DelegateList(generics.ListCreateAPIView, ListUpdateModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (permissions.DelegateListPermission, )
    serializer_class = DelegateSerializer

    def get_queryset(self):
        queryset = Delegate.objects.all()
        query_params = self.request.GET

        school_id = query_params.get('school_id', None)
        if school_id:
            queryset = queryset.filter(school_id=school_id)

        committee_id = query_params.get('committee_id', None)
        if committee_id:
            queryset = queryset.filter(assignment__committee_id=committee_id)

        return queryset


class DelegateDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, )
    queryset = Delegate.objects.all()
    permission_classes = (permissions.DelegateDetailPermission, )
    serializer_class = DelegateSerializer

    def put(self, request, *args, **kwargs):
        return self.list_update(request, *args, **kwargs)


class DelegateDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Delegate.objects.all()
    permission_classes = (IsSchoolDelegateAdvisorOrSuperuser,)
    serializer_class = DelegateSerializer
