# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson

from huxley.core.models import *
from huxley.shortcuts import render_template


def summaries(request):
    """ Display the summaries page for chairs. """
    com = request.user.committee
    if request.method == 'POST':
        delegate_slots = simplejson.loads(request.POST['delegate_slots'])
        for slot_data in delegate_slots:
            delegate = Delegate.objects.get(delegate_slot=DelegateSlot.objects.get(id=slot_data['id']))
            delegate.summary = slot_data['textfield']
            delegate.save()
        return HttpResponse()
    delegate_slots = DelegateSlot.objects.filter(assignment__committee=com).order_by('assignment__country__name')
    return render_template(request, 'summaries.html', {'delegate_slots': delegate_slots})


def attendance(request):
    """ Display a page allowing the chair to take attendance. """
    committee = request.user.committee
    if request.method == 'POST':
        delegate_slots = simplejson.loads(request.POST['delegate_slots'])
        for slot_data in delegate_slots:
            slot = DelegateSlot.objects.get(id=slot_data['id'])
            slot.update_delegate_attendance(slot_data)
        return HttpResponse()

    delegate_slots = DelegateSlot.objects.filter(assignment__committee=committee).order_by('assignment__country__name')

    return render_template(request, 'take_attendance.html', {'delegate_slots': delegate_slots})


def help(request):
    """ Display a FAQ view. """
    questions = {category.name: HelpQuestion.objects.filter(category=category)
                 for category in HelpCategory.objects.all()}
    return render_template(request, 'help.html', {'categories': questions})


def bugs(request):
    """ Display a bug reporting view. """
    return render_template(request, 'bugs.html')
