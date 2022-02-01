# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).
import json

from datetime import timedelta

from django.urls import reverse
from django.shortcuts import redirect, render
from django.template import RequestContext

from huxley.api.serializers import UserSerializer
from huxley.core.constants import ContactGender, ContactType, ProgramTypes
from huxley.core.models import Conference


def makeFullDate(date):
    day = date.strftime('%d')
    if day[0] == "0":
        day = day[1:]
    return {
        'month': date.strftime('%B'),
        'day': day,
        'year': date.strftime('%Y')
    }


def makeFullDateJSON(date):
    return (date.isoformat()+" 23:59:59 GMT-0700")


def makeShortDate(date):
    day = date.strftime('%d')
    month = date.strftime('%m')
    if day[0] == "0":
        day = day[1:]
    if month[0] == "0":
        month = month[1:]
    return month + "/" + day

# get the date from models by doing conference.
# then parse it into a js object


def index(request):
    if request.user.is_superuser:
        return redirect(reverse('admin:index'))

    user_dict = {}
    if request.user.is_authenticated:
        user_dict = UserSerializer(request.user).data

    conference = Conference.get_current()

    conference_dict = {
        'session': conference.session,
        'start_date': makeFullDate(conference.start_date),
        'end_date': makeFullDate(conference.end_date),
        'reg_open': makeShortDate(conference.reg_open),
        'round_one_end': makeShortDate(conference.round_one_end),
        'round_one_fees_due': makeShortDate(conference.round_one_fees_due),
        'round_two_start': makeShortDate(conference.round_one_end + timedelta(days=1)),
        'round_two_end': makeShortDate(conference.round_two_end),
        'round_two_fees_due': makeShortDate(conference.round_two_fees_due),
        'round_three_start': makeShortDate(conference.round_two_end + timedelta(days=1)),
        'round_three_end': makeShortDate(conference.round_three_end),
        'round_three_fees_due': makeShortDate(conference.round_three_fees_due),
        'round_four_start': makeShortDate(conference.round_three_end + timedelta(days=1)),
        'reg_close': makeShortDate(conference.reg_close),
        'round_four_fees_due': makeShortDate(conference.round_four_fees_due),
        'part_refund_deadline': makeShortDate(conference.part_refund_deadline),
        'early_paper_deadline': makeFullDate(conference.early_paper_deadline),
        'paper_deadline':  makeFullDate(conference.paper_deadline),
        'waiver_avail_date': makeShortDate(conference.waiver_avail_date),
        'waiver_deadline': makeShortDate(conference.waiver_deadline),
        'waiver_link': conference.waiver_link,
        'external': conference.external,
        'treasurer': conference.treasurer,
        'registration_fee': int(conference.registration_fee),
        'delegate_fee': int(conference.delegate_fee),
        'registration_open': conference.open_reg,
        'registration_waitlist': conference.waitlist_reg,
        'position_papers_accepted': conference.position_papers_accepted,
        'notes_enabled': conference.notes_enabled,
        'opi_link': conference.opi_link,
        'polling_interval': conference.polling_interval,
        'max_refresh_interval': conference.max_refresh_interval,
        'note_checkpoint_padding': conference.note_checkpoint_padding,
        'advisor_edit_deadline': makeFullDateJSON(conference.advisor_edit_deadline)
    }
    # need to parse dates to int in dictionary above
    # need to write a new parsing function to pass data to frontend

    context = {
        'user_json': json.dumps(user_dict).replace('</', '<\\/'),
        'conference_json': json.dumps(conference_dict),
        'gender_constants': ContactGender.to_json(),
        'contact_types': ContactType.to_json(),
        'program_types': ProgramTypes.to_json(),
    }

    return render(request, 'www.html', context)
