# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.accounts.models import HuxleyUser
from huxley.api.permissions import IsSuperuserOrReadOnly, IsUserOrSuperuser
from huxley.api.serializers import (CommitteeSerializer, CountrySerializer,
                                    UserSerializer)
from huxley.core.models import Committee, Country

class UserList(generics.ListCreateAPIView):
    queryset = HuxleyUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
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

class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsSuperuserOrReadOnly,)

class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsSuperuserOrReadOnly,)
