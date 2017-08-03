# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api.serializers import RegistrationSerializer
from huxley.core.models import Registration


class RegistrationList(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
