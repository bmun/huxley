# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson

from huxley.core.models import *
from huxley.shortcuts import render_template


def grading(request):
    """ Display the grading page for chairs. """
    return render_to_response('comingsoon.html')


def attendance(request):
    """ Display a page allowing the chair to take attendance. """
    committee = profile.committee
    if request.method == 'POST':
        delegate_slots = simplejson.loads(request.POST['delegate_slots'])
        for slot_data in delegate_slots:
            slot = DelegateSlot.objects.get(id=slot_data['id'])
            slot.update_delegate_attendance(slot_data)
        return HttpResponse()

    delegate_slots = DelegateSlot.objects \
                                 .filter(assignment__committee=committee) \
                                 .order_by('assignment__country')

    return render_template(request,
                           'take_attendance.html',
                           {'delegate_slots': delegate_slots,
                            'committee': committee})


def help(request):
    """ Display a FAQ view. """
    questions = {category.name: HelpQuestion.objects.filter(category=category)
                 for category in HelpCategory.objects.all()}
    return render_template(request, 'help.html', {'categories': questions})


def bugs(request):
    """ Display a bug reporting view. """
    return render_template(request, 'bugs.html')
