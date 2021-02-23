# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api import permissions
from huxley.api.serializers import CommitteeSerializer
from huxley.core.models import Committee


class CommitteeList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer


class CommitteeDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = Committee.objects.all()
    permission_classes = (permissions.CommitteeDetailPermission, )
    serializer_class = CommitteeSerializer

    def patch(self, request, *args, **kwargs):
        return super().patch(request, args, kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
