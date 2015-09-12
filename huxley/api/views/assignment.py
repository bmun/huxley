# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from huxley.api.permissions import IsSchoolAdvisorOrSuperuser, IsSuperuserOrReadOnly
from huxley.api.serializers import AssignmentSerializer
from huxley.core.models import Assignment


class AssignmentList(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Assignment.objects.all()
    permission_classes = (IsSuperuserOrReadOnly,)
    serializer_class = AssignmentSerializer


class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Assignment.objects.all()
    permission_classes = (IsSchoolAdvisorOrSuperuser,)
    serializer_class = AssignmentSerializer


class AssignmentDelete(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsSchoolAdvisorOrSuperuser,)

    def post(self, request, *args, **kwargs):
        assignment_id = kwargs.get('pk', None)
        assignment = Assignment.objects.get(id=assignment_id)
        assignment.delete()

        return Response(status=status.HTTP_200_OK)

