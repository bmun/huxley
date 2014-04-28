# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.accounts.models import HuxleyUser
from huxley.api.permissions import IsPostOrSuperuserOnly, IsUserOrSuperuser
from huxley.api.serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = HuxleyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsPostOrSuperuserOnly,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = HuxleyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrSuperuser,)
