# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api import permissions
from huxley.api.serializers import RubricSerializer
from huxley.core.models import Rubric


class RubricDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (SessionAuthentication, )
    queryset = Rubric.objects.all()
    permission_classes = (permissions.RubricDetailPermission, )
    serializer_class = RubricSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
