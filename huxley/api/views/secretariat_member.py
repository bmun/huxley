# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api.serializers import SecretariatMemberSerializer

from huxley.core.models import SecretariatMember


class SecretariatMemberList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, )
    queryset = SecretariatMember.objects.all()
    serializer_class = SecretariatMemberSerializer


class SecretariatMemberCommitteeList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, )
    serializer_class = SecretariatMemberSerializer

    def get_queryset(self):
        query_params = self.request.GET

        committee_id = query_params.get('committee_id', None)
        if committee_id:
            return SecretariatMember.objects.filter(committee_id=committee_id)
        else:
            return SecretariatMember.objects.none()


class SecretariatMemberDetail(generics.RetrieveAPIView):
    authentication_classes = (SessionAuthentication, )
    queryset = SecretariatMember.objects.all()
    serializer_class = SecretariatMemberSerializer
