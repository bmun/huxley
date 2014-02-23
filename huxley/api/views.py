# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from rest_framework import generics

from huxley.accounts.models import HuxleyUser
from huxley.api.permissions import IsSuperuserOrReadOnly, IsUserOrSuperuser
from huxley.api.serializers import CommitteeSerializer, UserSerializer
from huxley.core.models import Committee

class UserList(generics.ListCreateAPIView):
    queryset = HuxleyUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HuxleyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrSuperuser,)

class CommitteeList(generics.ListCreateAPIView):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer
    permission_classes = (IsSuperuserOrReadOnly,)

class CommitteeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer
    permission_classes = (IsSuperuserOrReadOnly,)
