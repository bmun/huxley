# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api import permissions
from huxley.api.serializers import AssignmentSerializer
from huxley.core.models import Assignment


class AssignmentList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.AssignmentListPermission,)
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        queryset = Assignment.objects.all()
        query_params = self.request.GET

        school_id = query_params.get('school_id', None)
        if school_id:
            queryset = queryset.filter(school_id=school_id)

        return queryset


class AssignmentDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Assignment.objects.all()
    permission_classes = (permissions.IsSchoolAssignmentAdvisorOrSuperuser,)
    serializer_class = AssignmentSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
