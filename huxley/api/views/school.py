
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
from huxley.api.permissions import IsAdvisorOrSuperuser, IsSchoolAdvisorOrSuperuser
from huxley.api.serializers import AssignmentSerializer, SchoolSerializer
from huxley.core.models import Assignment, School

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

<<<<<<< 5d3a71fa59dc25788b33464de26c80d1c46a7b39
=======
class SchoolAssignmentsFinalize(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsSchoolAdvisorOrSuperuser,)

    def post(self, request, *args, **kwargs):
        school_id = self.kwargs.get('pk', None)
        school = School.objects.get(id=school_id)
        school.assignments_finalized = True
        school.save()
        data = json.load(request)
        for identity in data:
            assignment = Assignment.objects.get(pk=int(identity))
            assignment.delete()

        return Response(status=status.HTTP_200_OK)

class SchoolInvoice(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsSchoolAdvisorOrSuperuser,)
>>>>>>> adds in api work for finalized assignments

class SchoolInvoice(PDFTemplateView):

    def get(self, request, *args, **kwargs):
        template_name = "invoice.html"

        school = School.objects.get(pk=kwargs['pk'])
        due_date = school.registered + datetime.timedelta(days=21)
        delegate_total = sum((
            school.beginner_delegates,
            school.intermediate_delegates,
            school.advanced_delegates,
        ))
        delegate_fees = delegate_total*School.DELEGATE_FEE
        fees_owed = school.fees_owed
        fees_paid = school.fees_paid
        amount_due = fees_owed - fees_paid

        context = Context({
            "name": school.name,
            "date_registered": school.registered.strftime("%m/%d/%y"),
            "due_date": due_date.strftime("%m/%d/%y"),
            "delegate_total": delegate_total,
            "delegate_fee": School.DELEGATE_FEE,
            "delegate_fees": delegate_fees,
            "registration_fee": School.REGISTRATION_FEE,
            "fees_owed": fees_owed,
            "fees_paid": fees_paid,
            "amount_due": amount_due})

        return render_to_pdf_response(request, template_name, context, **kwargs)


