# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
import rest_framework

from huxley.api.permissions import IsChairOrSuperuser, IsSchoolAssignmentAdvisorOrSuperuser, IsSuperuserOrReadOnly
from huxley.api.serializers import AssignmentSerializer
from huxley.core.models import Assignment


class AssignmentList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = [rest_framework.permissions.AllowAny,]
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        '''Filter assignments by the given assignment_id param.'''
        assignment_id = self.request.query_params.get('assignment_id', None)
        if assignment_id:
            return Assignment.objects.filter(assignment_id=assignment_id)
        return Assignment.objects.all()


class AssignmentDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Assignment.objects.all()
    permission_classes = (IsSchoolAssignmentAdvisorOrSuperuser,)
    serializer_class = AssignmentSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
