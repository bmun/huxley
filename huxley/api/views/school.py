# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import datetime

from easy_pdf.views import PDFTemplateView
from django.http import Http404
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from huxley.api import permissions
from huxley.api.serializers import DelegateSerializer, SchoolSerializer
from huxley.core.models import Conference, Delegate, School


class SchoolList(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = (permissions.SchoolDetailPermission,)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class SchoolInvoice(PDFTemplateView):
    template_name = 'invoice.html'

    def get_context_data(self, **kwargs):
        conference = Conference.get_current()
        school = School.objects.get(pk=kwargs['pk'])
        due_date = school.registered + datetime.timedelta(days=21)
        delegate_total = sum((
            school.beginner_delegates,
            school.intermediate_delegates,
            school.advanced_delegates,
        ))
        delegate_fee = conference.delegate_fee
        delegate_fees = delegate_total * delegate_fee
        fees_owed = school.fees_owed
        fees_paid = school.fees_paid
        amount_due = fees_owed - fees_paid

        return super(SchoolInvoice, self).get_context_data(
            name=school.name,
            date_registered=school.registered.strftime("%m/%d/%y"),
            due_date=due_date.strftime("%m/%d/%y"),
            delegate_total=delegate_total,
            delegate_fee=delegate_fee,
            delegate_fees=delegate_fees,
            registration_fee=conference.registration_fee,
            fees_owed=fees_owed,
            fees_paid=fees_paid,
            amount_due=amount_due,
            **kwargs
        )
