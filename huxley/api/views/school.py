# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import datetime

from easy_pdf.views import PDFTemplateView
from easy_pdf.rendering import render_to_pdf_response
from django.conf import settings
from django.http import Http404
from django.template import Context
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from huxley.api.mixins import ListUpdateModelMixin
from huxley.api.permissions import IsAdvisorOrSuperuser, IsSchoolAdvisorOrSuperuser
from huxley.api.serializers import AssignmentSerializer, DelegateSerializer, SchoolSerializer
from huxley.core.models import Assignment, Conference, Delegate, School


class SchoolList(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = (IsAdvisorOrSuperuser,)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


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


class SchoolDelegates(generics.ListAPIView, ListUpdateModelMixin):
    authentication_classes = (SessionAuthentication,)
    serializer_class = DelegateSerializer
    permission_classes = (IsSchoolAdvisorOrSuperuser,)

    def get_queryset(self):
        '''Filter schools by the given pk param.'''
        school_id = self.kwargs.get('pk', None)
        if not school_id:
            raise Http404

        return Delegate.objects.filter(school_id=school_id)

    def put(self, request, *args, **kwargs):
        return self.list_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_list_update(request, *args, **kwargs)


class SchoolInvoice(PDFTemplateView):

    def get(self, request, *args, **kwargs):
        template_name = "invoice.html"

        conference = Conference.get_current()
        school = School.objects.get(pk=kwargs['pk'])
        due_date = school.registered + datetime.timedelta(days=21)
        delegate_total = sum((
            school.beginner_delegates,
            school.intermediate_delegates,
            school.advanced_delegates,
        ))
        delegate_fee = conference.delegate_fee
        delegate_fees = delegate_total*delegate_fee
        fees_owed = school.fees_owed
        fees_paid = school.fees_paid
        amount_due = fees_owed - fees_paid

        context = Context({
            "name": school.name,
            "date_registered": school.registered.strftime("%m/%d/%y"),
            "due_date": due_date.strftime("%m/%d/%y"),
            "delegate_total": delegate_total,
            "delegate_fee": delegate_fee,
            "delegate_fees": delegate_fees,
            "registration_fee": conference.registration_fee,
            "fees_owed": fees_owed,
            "fees_paid": fees_paid,
            "amount_due": amount_due})

        return render_to_pdf_response(request, template_name, context, **kwargs)


