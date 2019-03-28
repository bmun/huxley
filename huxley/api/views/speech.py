# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication


from huxley.api import permissions
from huxley.api.serializers import SpeechSerializer
from huxley.core.models import Speech

class SpeechList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (permissions.SpeechListPermission, )
    queryset = Speech.objects.all()
    serializer_class = SpeechSerializer
