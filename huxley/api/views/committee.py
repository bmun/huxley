# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics

from huxley.api.permissions import IsSuperuserOrReadOnly
from huxley.api.serializers import CommitteeSerializer
from huxley.core.models import Committee


class CommitteeList(generics.ListCreateAPIView):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer
    permission_classes = (IsSuperuserOrReadOnly,)


class CommitteeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer
    permission_classes = (IsSuperuserOrReadOnly,)
