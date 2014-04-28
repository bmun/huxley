# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api.permissions import IsSuperuserOrReadOnly
from huxley.api.serializers import CountrySerializer
from huxley.core.models import Country


class CountryList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsSuperuserOrReadOnly,)


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsSuperuserOrReadOnly,)
