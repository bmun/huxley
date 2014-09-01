# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api.permissions import IsAdvisorOrSuperuser
from huxley.api.serializers import SchoolSerializer
from huxley.core.models import School


class SchoolList(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def create(self, request, *args, **kwargs):
        '''Intercept the create request and extract the country preference data,
        create the school as normal, then create the country preferences.

        This is a workaround for Django Rest Framework not supporting M2M
        fields with a "through" model.'''
        country_ids = request.DATA.pop('country_preferences', [])
        response = super(SchoolList, self).create(request, *args, **kwargs)
        school_id = response.data.get('id')

        if school_id:
            prefs = School.update_country_preferences(school_id, country_ids)
            response.data['country_preferences'] = prefs

        return response


class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = (IsAdvisorOrSuperuser,)
