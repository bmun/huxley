# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.db.models import Max
from django.shortcuts import redirect

from huxley.api.serializers import UserSerializer
from huxley.core.constants import ContactGender, ContactType, ProgramTypes
from huxley.core.models import Conference
from huxley.utils.shortcuts import render_template


def index(request):
    if request.user.is_superuser:
        return redirect(reverse('admin:index'))

    user_dict = {};
    if request.user.is_authenticated():
        user_dict = UserSerializer(request.user).data

    conference = Conference.get_conference()

    conference_dict = {
        'session': conference.session,
        'start_date': {
            'month': conference.start_date.strftime('%B'),
            'day': conference.start_date.strftime('%d'),
            'year': conference.start_date.strftime('%Y')
        },
        'end_date': {
            'month': conference.end_date.strftime('%B'),
            'day': conference.end_date.strftime('%d'),
            'year': conference.end_date.strftime('%Y')
        },
        'external': conference.external,
        'registration_fee': int(conference.registration_fee),
        'delegate_fee': int(conference.delegate_fee)
    }

    context = {
        'user_json': json.dumps(user_dict).replace('</', '<\\/'),
        'conference_json': json.dumps(conference_dict),
        'gender_constants': ContactGender.to_json(),
        'contact_types': ContactType.to_json(),
        'program_types': ProgramTypes.to_json(),
    }

    return render_template(request, 'www.html', context)
