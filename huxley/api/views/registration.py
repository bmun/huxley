# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api.permissions import RegistrationDetailPermission, RegistrationListPermission
from huxley.api.serializers import RegistrationSerializer
from huxley.core.models import Registration


class RegistrationList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, )
    serializer_class = RegistrationSerializer
    permission_classes = (RegistrationListPermission, )

    def get_queryset(self):
        queryset = Registration.objects.all()
        query_params = self.request.GET

        school_id = query_params.get('school_id', None)
        conference_session = query_params.get('conference_id', None)
        if school_id and conference_session:
            queryset = queryset.filter(
                school_id=school_id, conference_id=conference_session)

        return queryset


class RegistrationDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, )
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (RegistrationDetailPermission, )
