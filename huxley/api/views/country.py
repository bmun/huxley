# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api.serializers import CountrySerializer
from huxley.core.models import Country


class CountryList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetail(generics.RetrieveAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
