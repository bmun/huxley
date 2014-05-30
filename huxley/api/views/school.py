# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api.permissions import IsAdvisorOrSuperuser, IsPostOrSuperuserOnly
from huxley.api.serializers import SchoolSerializer
from huxley.core.models import School


class SchoolList(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = (IsPostOrSuperuserOnly,)


class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = (IsAdvisorOrSuperuser,)
