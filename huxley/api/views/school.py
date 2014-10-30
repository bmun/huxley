
# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.http import Http404
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from huxley.api.permissions import IsAdvisorOrSuperuser, IsSchoolAdvisorOrSuperuser
from huxley.api.serializers import AssignmentSerializer, SchoolSerializer
from huxley.core.models import Assignment, School

import datetime
import requests
import json

class SchoolList(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


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

class SchoolInvoice(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)

    def invoice_date(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d")

    def get_contact(self, school_name):
      list_url = 'https://invoice.zoho.com/api/v3/contacts?organization_id=41668886&authtoken=bf583d135a5a677a9a85ec1bc8268ab8'
      contact = {
        "company_name_contains": school_name
      }
      customer_id = requests.get(list_url, params=contact).json()["contacts"][0]["contact_id"]

      get_url = 'https://invoice.zoho.com/api/v3/contacts/' + customer_id + '?organization_id=41668886&authtoken=bf583d135a5a677a9a85ec1bc8268ab8'
      contact_id = requests.get(get_url).json()["contact"]["primary_contact_id"]
      return (customer_id, contact_id)

    def post(self, request, *args, **kwargs):
        vals = dict(request.DATA.iterlists())
        vals = dict([(str(k), str(v[0])) for k, v in vals.items()])

        customer_id, contact_id = self.get_contact(vals["school.name"])
        attrs = {
          "customer_id": customer_id,
          "contact_persons":  [
            contact_id,
          ],
          "invoice_number": "",
          "template_id": "",
          "date": self.invoice_date(),
          "payment_terms": 100,
          "payment_terms_label": "Due on Receipt",
          "due_date": "2015-02-27",
          "discount": 0.00,
          "is_discount_before_tax": True,
          "discount_type": "item_level",
          "exchange_rate": 1.00,
          "recurring_invoice_id": "",
          "salesperson_name": "",
          "custom_fields": [
          ],
          "line_items": [
            {
              "item_id": "",
              "project_id": "",
              "expense_id": "",
              "name": "Conference Registration Fee",
              "description": "Conference registration for a school, including school fee and delegate fees.",
              "rate": int(vals['school.fees_owed']),
              "unit": "",
              "quantity": 1.00,
              "discount": 0.00,
              "tax_id": ""
            },
          ],
          "payment_options": {
          },
          "allow_partial_payments": True,
          "shipping_charge": 0.00,
          "adjustment": -int(vals['school.fees_paid']),
          "adjustment_description": "Already Paid",
        }
        parameters = {
            "send": True,
            "ignore_auto_number_generation": False,
            "JSONString": json.dumps(attrs)
        }
        zoho_url = 'https://invoice.zoho.com/api/v3/invoices?organization_id=41668886&authtoken=bf583d135a5a677a9a85ec1bc8268ab8'
        r = requests.post(zoho_url, params=parameters)
        return Response(status=status.HTTP_201_CREATED)
