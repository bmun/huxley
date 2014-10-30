# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json
import requests

from django.conf import settings

def get_contact(school):
    if settings.ZOHO_CREDENTIALS:
        return
    list_url = 'https://invoice.zoho.com/api/v3/contacts?organization_id=' + settings.ORGANIZATION_ID + '&authtoken=' + settings.AUTHTOKEN
    contact = {
        "company_name_contains": school.name
    }
    return requests.get(list_url, params=contact).json()["contacts"][0]["contact_id"]

def generate_contact_attributes(school):
    return {
        "contact_name": school.primary_name,
        "company_name": school.name,
        "payment_terms": "",
        "payment_terms_label": "Due on Receipt",
        "currency_id": "",
        "website": "",
        "custom_fields": [
        ],
        "billing_address": {
        "address": "",
        "city": "",
        "state": "",
        "zip": "",
        "country": "",
        "fax": ""
        },
        "shipping_address": {
        "address": "",
        "city": "",
        "state": "",
        "zip": "",
        "country": "",
        "fax": ""
        },
        "contact_persons": [{
          "salutation": "",
          "first_name": "",
          "last_name": "",
          "email": school.primary_email,
          "phone": "",
          "mobile": "",
          "is_primary_contact": True
        }],
        "default_templates": {
        "invoice_template_id": "",
        "estimate_template_id": "",
        "creditnote_template_id": "",
        "invoice_email_template_id": "",
        "estimate_email_template_id": "",
        "creditnote_email_template_id": ""
        },
        "notes": ""
    }
