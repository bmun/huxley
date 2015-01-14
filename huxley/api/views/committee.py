# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api.serializers import CommitteeSerializer
from huxley.core.models import Committee


class CommitteeList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer


class CommitteeDetail(generics.RetrieveAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer
