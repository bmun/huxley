# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from huxley.api.permissions import IsSchoolDelegateAdvisorOrSuperuser, IsSuperuserOrReadOnly
from huxley.api.serializers import DelegateSerializer
from huxley.core.models import Delegate


class DelegateList(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Delegate.objects.all()
    permission_classes = (IsSuperuserOrReadOnly,)
    serializer_class = DelegateSerializer


class DelegateDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Delegate.objects.all()
    permission_classes = (IsSchoolDelegateAdvisorOrSuperuser,)
    serializer_class = DelegateSerializer
