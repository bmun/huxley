# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.http import Http404
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api.permissions import IsAdvisorOrSuperuser, IsSchoolAdvisorOrSuperuser
from huxley.api.serializers import AssignmentSerializer, SchoolSerializer
from huxley.core.models import Assignment, School


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


class SchoolAssignments(generics.ListAPIView):
    authentication_classes = (SessionAuthentication,)
    serializer_class = AssignmentSerializer
    permission_classes = (IsSchoolAdvisorOrSuperuser,)

    def get_queryset(self):
        '''Filter schools by the given pk param.'''
        school_id = self.kwargs.get('pk', None)
        if not school_id:
            raise Http404

        return Assignment.objects.filter(school_id=school_id)
